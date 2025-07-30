import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QDateTimeEdit,
                                QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
                                  QFileDialog, QHBoxLayout, QFrame, QComboBox)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon

from obspy import UTCDateTime
from downloader import EarthquakeDownloader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from seisy.core.custom_classes import CustomSplitter, DropPlotCanvas, CustomNavigationToolbar
from PyQt5.QtCore import QThread, pyqtSignal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from seisd import __app_name__, __version__
from realtime_downloader import ControlPanel,RealTimeSeismicPlotter

class CustomDateFormatter(mdates.DateFormatter):
    def __init__(self, fmt='%Y-%m-%d %H:%M:%S', short_fmt='%H:%M'):
        super().__init__(fmt)
        self.fmt = fmt
        self.short_fmt = short_fmt
        self.prev_date = None

    def __call__(self, x, pos=None):
        date = mdates.num2date(x).date()
        if date != self.prev_date:
            self.prev_date = date
            return mdates.num2date(x).strftime(self.fmt)
        else:
            return mdates.num2date(x).strftime(self.short_fmt)

class DownloadThread(QThread):
    result_ready = pyqtSignal(str, object)  # Signal to send the result and the stream

    def __init__(self,parent=None, downloader=None, network=None, station=None, location=None, channel=None,
                  starttime=None, endtime=None, steptime=24, file_format="MSEED"):
        super().__init__()
        self.parent = parent
        self.downloader = downloader
        self.network = network
        self.station = station
        self.location = location
        self.channel = channel
        self.starttime = starttime
        self.endtime = endtime
        self.steptime = steptime
        self.file_format = file_format
        self._stop_requested = False  # 添加标志位
        
    def generate_filename(self,current_time, next_day):
        # 使用 .strftime() 方法将时间格式化为 "YYYYMMDD_HHMMSS"
        start_time_str = current_time.strftime("%Y%m%d_%H%M%S")
        end_time_str = next_day.strftime("%Y%m%d_%H%M%S")
        
        # 创建文件名格式：network.station.channel.start_time-end_time.mseed
        if self.channel =="*":
            self.channel = "_"
        if self.location =="*":
            self.location = "_"
    
        filename = f"{self.network}.{self.station}.{self.location}.{self.channel}.{start_time_str}-{end_time_str}.{self.file_format.lower()}"
        return filename

    def run(self):
        try:
            current_time = self.starttime

            while current_time < self.endtime and not self._stop_requested:
                next_day = current_time + int(self.steptime * 3600)  # 加上步长时间（小时）
                if next_day > self.endtime or int(self.steptime) < 1e-3:
                    next_day = self.endtime

                # 生成符合要求的文件名
                filename = self.generate_filename(current_time, next_day)
                filename = self.sanitize_filename(filename)
                filename = os.path.join(self.parent.savedata_path, filename)

                if self._stop_requested:
                    break  # 如果已经请求停止，则退出

                result, st = self.downloader.download_waveforms(
                    self.network, self.station, self.location, self.channel, current_time, next_day, filename, self.file_format)

                self.result_ready.emit(result, st)  # 发送结果和数据流到主线程

                current_time = next_day

                if self._stop_requested:
                    break  # 每次操作后检查停止标志

        except Exception as e:
            # 处理任何可能的异常，确保线程能够优雅退出
            self.result_ready.emit(f"Error: {str(e)}", None)
        finally:
            # 确保在任何情况下都会发出完成或停止信号
            self.result_ready.emit("Download complete or stopped.", None)

    def sanitize_filename(self, filename):
        return "".join(c for c in filename if c.isalnum() or c in ('.', '_','-')).rstrip()
    
    def stop(self):
        """标志位设置为True，通知线程停止"""
        self._stop_requested = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.theme_fg = "black"
        self.theme_bg = "#EEEEEE"
        self.num = 0
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.set_window()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(os.path.join(self.script_dir, 'icons','SeisD.png')))

        self.showMaximized()

    def set_window(self):
        self.setWindowTitle("Earthquake Data Downloader")
        self.setGeometry(100, 100, 1600, 900)
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建主水平分割器
        self.top_splitter = CustomSplitter(Qt.Horizontal, [100, 250])

        self.downloader = EarthquakeDownloader()
        # 创建左侧分割器（上和下）
        self.left_splitter = CustomSplitter(Qt.Vertical, [300])
        self.left_top = QFrame()
        self.left_top.setFrameShape(QFrame.Box)
        self.left_top.setFrameShadow(QFrame.Raised)
        self.left_splitter.addWidget(self.left_top)
        self.left_splitter.setSizes(self.left_splitter.default_sizes)

        # 创建中间区域
        self.center_splitter = CustomSplitter(Qt.Vertical, [100, 100, 100])
        self.center_top = QFrame()
        self.center_top.setFrameShape(QFrame.Box)
        self.center_top.setFrameShadow(QFrame.Raised)
        self.center_mid = QFrame()
        self.center_mid.setFrameShape(QFrame.Box)
        self.center_mid.setFrameShadow(QFrame.Raised)
        self.center_bottom = QFrame()
        self.center_bottom.setFrameShape(QFrame.Box)
        self.center_bottom.setFrameShadow(QFrame.Raised)
        
        self.center_splitter.addWidget(self.center_top)
        self.center_splitter.addWidget(self.center_mid)
        self.center_splitter.addWidget(self.center_bottom)
        self.center_splitter.setSizes(self.center_splitter.default_sizes)

        # 将左侧、中间和右侧分割器添加到主分割器
        self.top_splitter.addWidget(self.left_splitter)
        self.top_splitter.addWidget(self.center_splitter)
        self.top_splitter.setSizes(self.top_splitter.default_sizes)
        # 设置背景颜色以区分区域
        self.set_background_color(self.central_widget, QColor(self.theme_bg))

        # 设置主布局
        self.main_splitter = CustomSplitter(Qt.Vertical, [300, 100])

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 5, 0, 0)  # 设置主布局边距为0
        self.main_layout.setSpacing(0)  # 设置主布局间距为0
        self.main_layout.addWidget(self.main_splitter)
        
        self.main_splitter.addWidget(self.top_splitter)

        self.realtime_waveforms()

        self.left_top_layout = QVBoxLayout(self.left_top)
        
        self.client_layout = QHBoxLayout()
        self.network_layout = QHBoxLayout()
        self.station_layout = QHBoxLayout()
        self.location_layout = QHBoxLayout()
        self.channel_layout = QHBoxLayout()
        self.starttime_layout = QHBoxLayout()
        self.endtime_layout = QHBoxLayout()
        self.steptime_layout = QHBoxLayout()
        self.download_layout = QHBoxLayout()
        self.magnitude_layout = QHBoxLayout()
        self.output_directory_layout = QHBoxLayout()
        self.file_format_layout = QHBoxLayout()


        self.setup_center_frame()

        self.client_combobox = QComboBox()
        self.client_combobox.addItems(["IRIS", "USGS", "GEOFON"])
        self.client_layout.addWidget(QLabel("Client:"))
        self.client_layout.addWidget(self.client_combobox)

        self.label_network = QLabel("Network:")
        self.input_network = QLineEdit("XA")
        self.network_layout.addWidget(self.label_network)
        self.network_layout.addWidget(self.input_network)
        
        self.label_station = QLabel("Station:")
        self.input_station = QLineEdit("S12")
        self.station_layout.addWidget(self.label_station)
        self.station_layout.addWidget(self.input_station)
        
        self.label_location = QLabel("Location:")
        self.input_location = QLineEdit("00")
        self.location_layout.addWidget(self.label_location)
        self.location_layout.addWidget(self.input_location)
        
        self.label_channel = QLabel("Channel:")
        self.input_channel = QLineEdit("MHZ")
        self.channel_layout.addWidget(self.label_channel)
        self.channel_layout.addWidget(self.input_channel)
        
        self.label_starttime = QLabel("Start Time:")
        self.input_starttime = QDateTimeEdit(QDateTime(1972, 12, 10, 8, 0, 0, 0))
        # self.input_starttime = QDateTimeEdit(QDateTime.currentDateTime())
        self.input_starttime.setCalendarPopup(True)
        self.input_starttime.setDisplayFormat("yyyy-MM-dd HH:mm:ss.zzz")
        self.starttime_layout.addWidget(self.label_starttime)
        self.starttime_layout.addWidget(self.input_starttime)

        self.label_endtime = QLabel("End Time:")
        self.input_endtime = QDateTimeEdit(QDateTime(1972, 12, 11, 8, 0, 0, 0))
        # self.input_endtime = QDateTimeEdit(QDateTime.currentDateTime())
        self.input_endtime.setCalendarPopup(True)
        self.input_endtime.setDisplayFormat("yyyy-MM-dd HH:mm:ss.zzz")
        self.endtime_layout.addWidget(self.label_endtime)
        self.endtime_layout.addWidget(self.input_endtime)

        self.label_steptime = QLabel("StepTime(h):")
        self.input_steptime = QLineEdit("24")
        self.steptime_layout.addWidget(self.label_steptime)
        self.steptime_layout.addWidget(self.input_steptime)

        self.button_download_waveforms = QPushButton("Downloading Waveforms")
        self.button_download_waveforms.clicked.connect(self.download_waveforms)
        self.button_stop_waveforms = QPushButton("Stop Downloading")
        self.button_stop_waveforms.clicked.connect(self.stop_download_waveforms)
        self.download_layout.addWidget(self.button_download_waveforms)
        self.download_layout.addWidget(self.button_stop_waveforms)
        
        self.label_min_magnitude = QLabel("Minimum Magnitude:")
        self.input_min_magnitude = QLineEdit("5.0")
        self.magnitude_layout.addWidget(self.label_min_magnitude)
        self.magnitude_layout.addWidget(self.input_min_magnitude)
        
        self.label_output_directory = QLabel("Output Directory:")
        self.input_output_directory = QLineEdit(f"{self.path}\data")
        self.output_directory_layout.addWidget(self.label_output_directory)

        self.button_browse_directory = QPushButton("Browse")
        self.button_browse_directory.clicked.connect(self.browse_directory)
        self.output_directory_layout.addWidget(self.button_browse_directory)        

        self.file_format_combobox = QComboBox()
        self.file_format_combobox.addItems(["MSEED", "SAC", "SEGY", "WAV"])
        self.file_format_layout.addWidget(QLabel("File Format:"))
        self.file_format_layout.addWidget(self.file_format_combobox)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.left_top_layout.addLayout(self.client_layout)
        self.left_top_layout.addLayout(self.network_layout)
        self.left_top_layout.addLayout(self.station_layout)
        self.left_top_layout.addLayout(self.location_layout)
        self.left_top_layout.addLayout(self.channel_layout)
        self.left_top_layout.addLayout(self.starttime_layout)
        self.left_top_layout.addLayout(self.endtime_layout)
        self.left_top_layout.addLayout(self.steptime_layout)
        self.left_top_layout.addLayout(self.magnitude_layout)
        self.left_top_layout.addLayout(self.output_directory_layout)
        self.left_top_layout.addWidget(self.input_output_directory)
        self.left_top_layout.addLayout(self.file_format_layout)
        self.left_top_layout.addLayout(self.download_layout)
        self.left_top_layout.addWidget(self.output_text)

        # 设置字体
        font = QFont()
        font.setFamily("Consolas") 
        font.setPointSize(11)
        self.main_splitter.setFont(font)

    def setup_center_frame(self):
        # 设置 center_top 布局
        self.center_top_layout = QVBoxLayout(self.center_top)
        self.center_top_layout.setContentsMargins(0, 0, 0, 0)
        self.center_top_layout.setSpacing(0)

        # 创建 Matplotlib 画布和导航工具栏（顶部）
        self.canvas_top = DropPlotCanvas(self, width=10, height=6, dpi=100)
        self.toolbar_top = CustomNavigationToolbar(self.canvas_top, self)

        # 将 Matplotlib 画布和导航工具栏添加到 center_top_layout
        self.center_top_layout.addWidget(self.toolbar_top)
        self.center_top_layout.addWidget(self.canvas_top)

        # 设置 center_mid 布局
        self.center_mid_layout = QVBoxLayout(self.center_mid)
        self.center_mid_layout.setContentsMargins(0, 0, 0, 0)
        self.center_mid_layout.setSpacing(0)

        # 创建 Matplotlib 画布和导航工具栏（中部）
        self.canvas_mid = DropPlotCanvas(self, width=10, height=6, dpi=100)
        self.toolbar_mid = CustomNavigationToolbar(self.canvas_mid, self)

        # 将 Matplotlib 画布和导航工具栏添加到 center_mid_layout
        self.center_mid_layout.addWidget(self.toolbar_mid)
        self.center_mid_layout.addWidget(self.canvas_mid)

        # 设置 center_bottom 布局
        self.center_bottom_layout = QVBoxLayout(self.center_bottom)
        self.center_bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.center_bottom_layout.setSpacing(0)

        # 创建 Matplotlib 画布和导航工具栏（底部）
        self.canvas_bottom = DropPlotCanvas(self, width=10, height=6, dpi=100)
        self.toolbar_bottom = CustomNavigationToolbar(self.canvas_bottom, self)

        # 将 Matplotlib 画布和导航工具栏添加到 center_bottom_layout
        self.center_bottom_layout.addWidget(self.toolbar_bottom)
        self.center_bottom_layout.addWidget(self.canvas_bottom)

    def set_background_color(self, widget, color):
        palette = widget.palette()
        palette.setColor(QPalette.Background, color)
        widget.setAutoFillBackground(True)
        widget.setPalette(palette)
        
    def sanitize_filename(self, filename):
        return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

    def download_waveforms(self):
        self.downloader.client = self.client_combobox.currentText()
        self.downloader.update_client()
        network = self.input_network.text()
        station = self.input_station.text()
        location = self.input_location.text()
        channel = self.input_channel.text()
        starttime = UTCDateTime(self.input_starttime.dateTime().toPyDateTime())
        endtime = UTCDateTime(self.input_endtime.dateTime().toPyDateTime())
        steptime = int(self.input_steptime.text())
        file_format = self.file_format_combobox.currentText()
        self.savedata_path = self.input_output_directory.text()

        self.canvas_order = [self.canvas_top, self.canvas_mid, self.canvas_bottom]
        self.canvas_index = 0

        # Create and start the download thread
        self.download_thread = DownloadThread(self,self.downloader, network, station, location, channel, starttime, endtime, steptime, file_format)
        self.download_thread.result_ready.connect(self.handle_download_result)
        self.download_thread.start()
    
    def stop_download_waveforms(self):
        if hasattr(self, 'download_thread') and self.download_thread.isRunning():
            self.download_thread.stop()
            self.download_thread.wait()  # 等待线程完全停止
            # self.output_text.append("Download thread stopped.")

    def handle_download_result(self, result, st):
        result = os.path.basename(result)
        if  "Download" in result:
            self.output_text.append(result)
        else:
            self.num = self.num  + 1
            self.output_text.append(f"{self.num}. {result}")

        if st:
            if self.canvas_index < len(self.canvas_order):
                self.plot_waveforms(st, self.canvas_order[self.canvas_index])
            else:
                self.update_canvas_order(st, self.canvas_order)
            
        self.canvas_index = (self.canvas_index + 1) % len(self.canvas_order)

    def update_canvas_order(self, stream, canvas_order):
        # 将当前的 canvas 图像下移
        for i in reversed(range(1, len(canvas_order))):
            canvas_order[i].fig.clear()
            for ax in canvas_order[i-1].fig.axes:
                canvas_order[i].fig._axstack.add_axes(ax)
            canvas_order[i].draw()

        # 在最上面的 canvas 上绘制新图像
        self.plot_waveforms(stream, canvas_order[0])

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.input_output_directory.setText(directory)
    
    def plot_waveforms(self, stream, canvas):
        canvas.fig.clear()
        
        for i, trace in enumerate(stream):
            ax = canvas.fig.add_subplot(len(stream), 1, i + 1)
            
            # 降采样以提高性能
            decimated_data = trace.data.copy()
            times = trace.times("matplotlib")
            decimated_times = times.copy()
            
            ax.plot(decimated_times, decimated_data, "k", antialiased=True, label=f"event_{self.num:03d}")  # 开启抗锯齿
            
            # 设置标题
            ax.set_title(f"{trace.id}", fontsize=10)

            # 设置横坐标为 UTC 时间显示
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(CustomDateFormatter('%Y-%m-%d %H:%M:%S', '%H:%M'))
            
            # 优化纵坐标的刻度数量
            ax.yaxis.set_major_locator(MaxNLocator(5))
            
            # 自动旋转日期标签
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center', fontsize=8)
        
        canvas.fig.tight_layout()
        canvas.fig.legend()
        canvas.draw()

    def realtime_waveforms(self):
        self.realtime_splitter = CustomSplitter(Qt.Horizontal, [50, 250])
        self.realtime_splitter.setMinimumHeight(250)  # 设置最小高度为200像素
        self.realtime_splitter.setMaximumHeight(500)  # 设置最大高度为500像素

        
        self.realtime_splitter.setSizes(self.realtime_splitter.default_sizes)

        self.control_panel = ControlPanel(self)
        self.plotter = RealTimeSeismicPlotter(self,control_panel=self.control_panel)

        # 设置control_panel和plotter的最小和最大宽度
        self.control_panel.setMinimumWidth(200)
        self.control_panel.setMaximumWidth(450)

        self.realtime_splitter.addWidget(self.control_panel)
        self.realtime_splitter.addWidget(self.plotter)
        self.main_splitter.addWidget(self.realtime_splitter)

def main():
    print("SeisD application started")
    # 这里添加你的应用程序启动逻辑
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
