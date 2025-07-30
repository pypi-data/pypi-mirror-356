import sys, os
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QLabel, 
                             QLineEdit, QComboBox, QDateTimeEdit, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QTimer, QDateTime
from PyQt5.QtCore import QThread, pyqtSlot, QObject
from PyQt5.QtGui import QIcon, QDoubleValidator, QFont
from seisy.core.custom_classes import NavigationToolbar

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FuncFormatter
from matplotlib.figure import Figure
from matplotlib.artist import Artist

from obspy.clients.seedlink.easyseedlink import create_client
from obspy.clients.fdsn import Client as FDSNClient
from obspy import Stream, UTCDateTime,Trace
from collections import deque
from datetime import timedelta, datetime, timezone
import logging
import time
import numpy as np
import traceback

class ControlPanel(QWidget):
    """左侧控制面板类"""
    settings_changed = pyqtSignal(dict)  # 创建一个信号，用于传递设置的变化

    def __init__(self, parent=None):
        super().__init__(parent)

        # 主垂直布局
        layout = QVBoxLayout()

        # 台网输入框
        network_station_layout = QHBoxLayout()
        network_label = QLabel("Network:")
        self.network_input = QLineEdit("IU")
        self.network_input.editingFinished.connect(self.emit_settings_changed)  # 连接到信号
        network_station_layout.addWidget(network_label)
        network_station_layout.addWidget(self.network_input)

        # 台站输入框
        station_label = QLabel("Station:")
        self.station_input = QLineEdit("MAJO")
        self.station_input.editingFinished.connect(self.emit_settings_changed)  # 连接到信号
        network_station_layout.addWidget(station_label)
        network_station_layout.addWidget(self.station_input)
        layout.addLayout(network_station_layout)

        # 位置输入框
        location_channel_layout = QHBoxLayout()
        location_label = QLabel("Location:")
        self.location_input = QLineEdit("00")
        self.location_input.editingFinished.connect(self.emit_settings_changed)  # 连接到信号
        location_channel_layout.addWidget(location_label)
        location_channel_layout.addWidget(self.location_input)

        # 通道输入框
        channel_label = QLabel("Channel:")
        self.channel_input = QLineEdit("BHZ")
        self.channel_input.editingFinished.connect(self.emit_settings_changed)  # 连接到信号
        location_channel_layout.addWidget(channel_label)
        location_channel_layout.addWidget(self.channel_input)
        layout.addLayout(location_channel_layout)

        # 服务器选择框
        server_layout = QHBoxLayout()
        server_label = QLabel("Server URL:")
        # 使用 QComboBox 替换 QLineEdit
        self.server_url_input = QComboBox()
        # 添加常见的 SeedLink 服务器选项
        self.server_url_input.addItems([
            "rtserve.iris.washington.edu",  # IRIS
            "geofon.gfz-potsdam.de",        # GEOFON
            "pubavo1.wr.usgs.gov",          # University of Alaska Fairbanks
            "rtserve.ncedc.org",            # NCEDC
            "rtserve.scedc.caltech.edu",    # SCEDC
            "eida.bgr.de",                  # Orfeus Data Center
            "seis3.kishou.go.jp"            # Japan Meteorological Agency (JMA)
        ])
        # 连接到信号，当用户选择服务器时触发
        self.server_url_input.currentIndexChanged.connect(self.emit_settings_changed)
        server_layout.addWidget(server_label)
        server_layout.addWidget(self.server_url_input)

        # 颜色选择框
        color_label = QLabel("Line Color:")
        self.color_combobox = QComboBox()
        self.color_combobox.addItems(['red', 'green', 'blue', 'white', 'gray', 'cyan', 'magenta', 'yellow', 'brown'])
        self.color_combobox.currentIndexChanged.connect(self.emit_settings_changed)  # 连接到信号
        server_layout.addWidget(color_label)
        server_layout.addWidget(self.color_combobox)
        layout.addLayout(server_layout)

        # 历史数据时间范围
        past_hours_layout = QHBoxLayout()
        past_hours_label = QLabel("Past Hours:")
        self.past_hours_input = QLineEdit("0.1")
        double_validator = QDoubleValidator(0.0, 100.0, 2, self)  # 最小值0.0, 最大值100.0, 小数点后最多2位
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        self.past_hours_input.setValidator(double_validator)
        self.past_hours_input.editingFinished.connect(self.update_start_time)  # 当时间范围改变时，更新开始时间
        self.past_hours_input.editingFinished.connect(self.emit_settings_changed)  # 连接到信号
        past_hours_layout.addWidget(past_hours_label)
        past_hours_layout.addWidget(self.past_hours_input)
        
        # 新增数据点个数设置
        npts_to_add_label = QLabel("Plot Speed:")
        self.npts_to_add_input = QLineEdit("20")
        npts_validator = QDoubleValidator(1, 200, 0, self)  # 最小值0.0, 最大值100.0
        npts_validator.setNotation(QDoubleValidator.StandardNotation)
        self.npts_to_add_input.setValidator(npts_validator)
        self.npts_to_add_input.editingFinished.connect(self.emit_settings_changed)  # 连接到信号
        past_hours_layout.addWidget(npts_to_add_label)
        past_hours_layout.addWidget(self.npts_to_add_input)

        # 画布更新速度设置
        ani_speed_label = QLabel("Ani Speed:")
        self.ani_speed_input = QLineEdit("500")
        ani_speed_validator = QDoubleValidator(1, 10000, 0, self)  # 最小值0.0, 最大值100.0, 小数点后最多2位
        ani_speed_validator.setNotation(QDoubleValidator.StandardNotation)
        self.ani_speed_input.setValidator(ani_speed_validator)
        self.ani_speed_input.editingFinished.connect(self.emit_settings_changed)  # 连接到信号
        past_hours_layout.addWidget(ani_speed_label)
        past_hours_layout.addWidget(self.ani_speed_input)
        layout.addLayout(past_hours_layout)   
  
        # 开始时间选择框
        start_time_layout = QHBoxLayout()
        start_time_label = QLabel("Initial Time (UTC):")
        self.start_time_input = QDateTimeEdit(QDateTime.currentDateTimeUtc())
        self.start_time_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.start_time_input.setReadOnly(True)  # 设置为只读
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(self.start_time_input)
        layout.addLayout(start_time_layout)

        # 结束时间（当前时间）选择框
        end_time_layout = QHBoxLayout()
        end_time_label = QLabel("Current Time (UTC):")
        self.end_time_input = QDateTimeEdit(QDateTime.currentDateTimeUtc())  # 设置为当前时间
        self.end_time_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.end_time_input.setReadOnly(True)  # 设置为只读
        self.end_time_input.dateTimeChanged.connect(self.update_start_time)  # 当当前时间改变时，更新开始时间
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addWidget(self.end_time_input)
        layout.addLayout(end_time_layout)

        # 设置定时器以实时更新时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(1000)  # 每隔1秒更新一次时间

        # 动画控制按钮
        button_layput = QHBoxLayout()
        self.refrensh_button = QPushButton("Refrensh Animation")
        self.toggle_button = QPushButton("Start/Pause Animation")
        button_layput.addWidget(self.refrensh_button)
        button_layput.addWidget(self.toggle_button)
        layout.addLayout(button_layput)

        # 设置主布局
        self.setLayout(layout)
        # 初始化开始时间
        self.update_start_time()

    def update_start_time(self):
        """根据当前时间和过去的小时数更新开始时间"""
        try:
            # 获取过去小时数
            past_hours = float(self.past_hours_input.text())
            
        except ValueError:
            # 如果输入不是有效数字，默认过去0.2小时
            past_hours = 0.2
        
        # 计算开始时间 = 结束时间 - 过去小时数
        end_time = self.end_time_input.dateTime().toPyDateTime()
        start_time = end_time - timedelta(hours=past_hours)
        self.start_time_input.setDateTime(QDateTime(start_time))

    def update_current_time(self):
        """更新 QDateTimeEdit 显示的当前时间"""
        self.end_time_input.setDateTime(QDateTime.currentDateTimeUtc())

    def emit_settings_changed(self):
        """发射设置变化的信号"""
        settings = self.get_settings()
        self.settings_changed.emit(settings)

    def get_settings(self):
        """返回所有用户输入的设置"""
        return {
            "network": self.network_input.text(),
            "station": self.station_input.text(),
            "location": self.location_input.text(),
            "channel": self.channel_input.text(),
            "server_url": self.server_url_input.currentText(),
            "past_hours": float(self.past_hours_input.text()),
            "start_time": UTCDateTime(self.start_time_input.dateTime().toPyDateTime()),
            "end_time": UTCDateTime(self.end_time_input.dateTime().toPyDateTime()),
            "line_color": self.color_combobox.currentText(),
            "npts_to_add": float(self.npts_to_add_input.text()),
            "ani_speed": float(self.ani_speed_input.text())
        }

class ThreadManager:
    def __init__(self, target, name="WorkerThread"):
        self.target = target
        self.thread = None
        self.stop_event = threading.Event()
        self.thread_name = name

    def start(self):
        print("prepare to start new Thread")
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()

            self.thread = threading.Thread(target=self.run_with_pause, name=self.thread_name)
            self.thread.daemon = True
            self.thread.start()
            # length = len(threading.enumerate())
            # logging.debug('当前运行的线程数为：%d' % length)
            # for thread in threading.enumerate():
            #     logging.debug(f"Thread name: {thread.name}, is_alive: {thread.is_alive()}, is_daemon: {thread.daemon}")

    def run_with_pause(self):
        while not self.stop_event.is_set():
            try:
                self.target()
            except Exception as e:
                logging.error(f"SeedLink client error: {e}")
                break  # 出现异常时退出循环
            if self.stop_event.is_set():
                break

    def stop(self, timeout=2):
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join(timeout=timeout)
            if self.thread.is_alive():
                logging.warning(f"{self.thread_name} did not stop in time.")
                self.thread.join(timeout=timeout)
            else:
                logging.debug(f"{self.thread_name} stopped.")
            self.thread = None

    def is_running(self):
        return self.thread is not None and self.thread.is_alive()

class SeedLinkDownloader:
    def __init__(self, server_url, network, station, location, channel, stream, handle_data_callback):
        self.server_url = server_url
        self.network = network
        self.station = station
        self.location = location
        self.channel = channel
        self.stream = stream
        self.seedlink_client = None
        self.stream_lock = threading.Lock()
        self.handle_data_callback = handle_data_callback

        # 使用 ThreadManager 管理下载线程
        self.thread_manager = ThreadManager(target=self.download_data, name=f"SeedLinkDownloadThread_{self.network}_{self.station}")

    def create_seedlink_client(self):
        location = "00" if self.location == "*" else self.location
        # print("---000---create_seedlink_client---\n", self.network, self.station, f"{location}{self.channel}")
        self.seedlink_client = create_client(self.server_url, on_data=lambda trace: self.handle_data_callback(trace))
        self.seedlink_client.select_stream(self.network, self.station, f"{location}{self.channel}")

    def download_data(self):
        self.seedlink_client.run()

        # retry_delay = 5  # 重试间隔时间（秒）
        # max_retries = 5  # 最大重试次数
        # retries = 0

        # while not self.thread_manager.stop_event.is_set() and retries < max_retries:
        #     try:
        #         logging.debug("Running SeedLink client...")
        #         self.seedlink_client.run()
        #         if self.thread_manager.stop_event.is_set():
        #             logging.debug("Pause event set, stopping download...")
        #             if self.seedlink_client:
        #                 self.seedlink_client.close()  
        #                 logging.debug("关闭连接，强制 run() 停止...")
        #             break
        #     except Exception as e:
        #         logging.error(f"SeedLink client error: {e}, retrying in {retry_delay}s")
        #         time.sleep(retry_delay)
        #         retries += 1
        #     if self.thread_manager.stop_event.is_set():
        #         break

        # logging.debug("Exiting download_data method.")

    def start_download(self):
        # print(f"{self.network}_{self.station}")
        self.thread_manager.thread_name = f"SeedLinkDownloadThread_{self.network}_{self.station}"
        self.create_seedlink_client()
        self.thread_manager.start()
        length = len(threading.enumerate())
        logging.debug('当前运行的线程数为：%d' % length)
        for thread in threading.enumerate():
            logging.debug(f"Thread name: {thread.name}, is_alive: {thread.is_alive()}, is_daemon: {thread.daemon}")

    def stop_download(self):
        if self.seedlink_client is not None:
            try:
                self.seedlink_client.conn.disconnect()

                if self.is_seedlink_client_connected():
                    logging.debug("SeedLink client is still connected.")
                    logging.debug("Preparing to close SeedLink client...")
                    self.seedlink_client.close()
                    logging.debug("SeedLink client closed successfully.")
                else:
                    logging.debug("SeedLink client is not connected or socket is closed.")
            except OSError as e:
                logging.error(f"Error closing SeedLink client: {e}")
            except Exception as e:
                logging.error(f"Unexpected error during SeedLink client close: {e}")
            finally:
                self.seedlink_client = None

        self.thread_manager.stop()

    def is_seedlink_client_connected(self):
        try:
            if self.seedlink_client is not None and self.seedlink_client.sock:
                self.seedlink_client.sock.send(b'\0')
                return True
        except Exception:
            return False
        return False

class SeismicDataDownloader:
    def __init__(self, server_url, network, station, location, channel, window_size=100, event_window_seconds=10):
        self.server_url = server_url
        self.network = network
        self.station = station
        self.location = location
        self.channel = channel
        self.stream = Stream()
        self.window_size = window_size
        self.amplitude_window = deque(maxlen=window_size)
        self.log_file = self.create_log_file()
        self.event_window_seconds = event_window_seconds
        self.last_event_time = None

        self.seedLink_downloader = SeedLinkDownloader(
            server_url, network, station, location, channel, self.stream, self.handle_data
        )
        self.stream_lock = self.seedLink_downloader.stream_lock
        self.stop_event = self.seedLink_downloader.thread_manager.stop_event

    def handle_data(self, trace):
        """处理实时到达的数据"""
        with self.stream_lock:
            logging.debug(f"Received trace: {trace.id} with {len(trace.data)} data points.")
            self.stream += trace
            self.stream.merge()
            # 如果需要监测地震活动，可以调用 monitor_seismic_activity(trace)
            # self.monitor_seismic_activity(trace)

    def start_download(self):
        self.seedLink_downloader.start_download()
        event_time = datetime.now(timezone.utc)
        self.show_warning_popup(event_time,1000,999)

    def stop_download(self):
        self.seedLink_downloader.stop_download()

    def update_station_info(self, network=None, station=None, location=None, channel=None):
        self.stop_download()

        if network:
            self.seedLink_downloader.network = network
        if station:
            self.seedLink_downloader.station = station
        if location:
            self.seedLink_downloader.location = location
        if channel:
            self.seedLink_downloader.channel = channel

        self.start_download()

    def monitor_seismic_activity(self, trace):
        """监测地震活动"""
        max_amplitude = max(abs(trace.data))
        self.amplitude_window.append(max_amplitude)
        
        if len(self.amplitude_window) == self.window_size:
            mean_amplitude = np.mean(self.amplitude_window)
            std_amplitude = np.std(self.amplitude_window)
            dynamic_threshold = mean_amplitude + 0.3 * std_amplitude  # 3倍标准差

            if max_amplitude > dynamic_threshold:
                event_time = datetime.now(timezone.utc)
                if self.last_event_time is None or (event_time - self.last_event_time >
                                                     timedelta(seconds=self.event_window_seconds)):
                    self.log_seismic_event(event_time, max_amplitude, dynamic_threshold)
                    self.create_event_directory(event_time, max_amplitude, dynamic_threshold)
                    self.show_warning_popup(event_time, max_amplitude, dynamic_threshold)

    def create_event_directory(self, event_time, max_amplitude, threshold):
        """创建地震事件目录并记录相关信息"""
        # 创建地震事件目录
        event_dir_name = event_time.strftime("%Y%m%d_%H%M%S")
        event_dir_path = os.path.join(os.getcwd(), f"earthquake_event_{event_dir_name}")
        os.makedirs(event_dir_path, exist_ok=True)

        # 创建地震事件日志文件
        event_log_file = os.path.join(event_dir_path, "event_log.txt")
        with open(event_log_file, 'a') as log:
            log.write(f"Event Time: {event_time.isoformat()}\n")
            log.write(f"Network: {self.network}\n")
            log.write(f"Station: {self.station}\n")
            log.write(f"Location: {self.location}\n")
            log.write(f"Channel: {self.channel}\n")
            log.write(f"Max Amplitude: {max_amplitude}\n")
            log.write(f"Threshold: {threshold}\n")
            log.write("\n")

        logging.info(f"Seismic event logged in {event_dir_path}")

        # 如果需要，可以在此保存更多的事件相关信息，例如可视化图表等
        # 例如保存一个振幅随时间变化的图表
        # self.save_amplitude_plot(event_dir_path)

    def log_seismic_event(self, event_time, max_amplitude, threshold):
        """记录地震事件"""
        with open(self.log_file, 'a') as log:
            log.write(f"{event_time.isoformat()} | Network: {self.network}, Station: {self.station}, Location: {self.location}, Channel: {self.channel}, "
                      f"Max Amplitude: {max_amplitude}, Threshold: {threshold}\n")
        logging.info(f"Seismic event detected and logged at {event_time.isoformat()} with amplitude {max_amplitude} (Threshold: {threshold})")

    def create_log_file(self):
        """创建地震监测日志文件"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"seismic_events_{self.network}_{self.station}_{self.location}_{self.channel}_{timestamp}.log"
        return os.path.join(os.getcwd(), filename)

    def show_warning_popup(self, event_time, max_amplitude, threshold):
        """在已有的 QApplication 实例中显示地震警告弹窗"""
        def _show_popup():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Seismic Event Detected")
            msg.setText("A seismic event has been detected!")
            msg.setInformativeText(f"Time: {event_time.isoformat()}\n"
                                f"Station: {self.station}\n"
                                f"Channel: {self.channel}\n"
                                f"Max Amplitude: {max_amplitude}\n"
                                f"Threshold: {threshold}")
            # 创建一个定时器，弹窗显示2秒后自动关闭
            QTimer.singleShot(2000, msg.accept)

            msg.exec_()

        # 创建一个新的线程来显示弹窗
        _show_popup()

        # threading.Thread(target=_show_popup, daemon=True).start()

class RealTimeSeismicPlotter(QWidget):
    def __init__(self, parent=None, control_panel=None):
        super().__init__(parent)
        self.control_panel = control_panel
        self.fdsn_client = FDSNClient("IRIS")
        self.network = None
        self.station = None
        self.location = None
        self.channel = None
        self.past_hours = None

        # 初始化图表配置
        self.stream_plot = Stream()
        self.trace = Trace()
        self.failed_intervals = deque()
        self.data_cache = []
        self.low_data_num = 0
        self.is_animation_running = False
        self.plotting = False
        self.downloader = None

        # 读取初始设置
        settings = self.control_panel.get_settings()
        self.update_settings(settings)

        # 初始化 Matplotlib 图表
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([], [], lw=0.5, color=self.line_color)
        self.ax.set_ylim(-1, 1)
        self.ax.set_title(f"Real-time Seismic Data (Past {self.past_hours} Hours)", color='white')
        self.ax.set_xlabel("Time (UTC)", color='white')
        self.ax.set_ylabel("Amplitude", color='white')
        self.ax.grid(True, color='gray')
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        # 初始文本对象的创建
        self.text_artist = self.ax.text(
            0.99, 0.95, "", transform=self.ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='left',
            bbox=dict(facecolor='white', alpha=0.8)
        )

        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # 初始化时间范围
        self.end_time = UTCDateTime()
        self.start_time = self.end_time - self.past_hours * 3600
        self.ax.set_xlim(self.start_time.timestamp, self.end_time.timestamp)

        # 设置自定义的 x 轴格式
        self.ax.xaxis.set_major_formatter(FuncFormatter(self.custom_xaxis_formatter))
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        # 下载过去的数据
        self.download_initial_data()

        # 创建并启动后台线程进行数据下载
        
        self.downloader = SeismicDataDownloader(self.server_url,self.network, self.station,
                                                self.location, self.channel)
        self.downloader.start_download()

        # 绑定控制面板的按钮事件
        self.control_panel.toggle_button.clicked.connect(self.toggle_animation)
        self.control_panel.refrensh_button.clicked.connect(self.refrensh_animation)
        self.control_panel.settings_changed.connect(self.update_settings)  # 连接设置变化信号

        # 启动动画
        self.ani = FuncAnimation(self.fig, self.update_plot, blit=False, 
                                 interval=self.ani_speed, cache_frame_data=False)
        self.is_animation_running = True

    def stop_all_operations(self):
        self.downloader.stop_download()
        if hasattr(self, 'ani') and self.is_animation_running:
            try:
                self.ani.event_source.stop()
                self.ani._stop()  # 尝试手动停止动画
                self.is_animation_running = False
            except Exception as e:
                print(f"Error stopping animation: {e}")

        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
            self.timer.deleteLater()

        if hasattr(self, 'canvas') and self.canvas is not None:
            self.canvas.deleteLater()

        if hasattr(self, 'fig') and self.fig is not None:
            plt.close(self.fig)

    def update_settings(self, settings):
        """更新设置"""
        # 检查台站信息是否有变化
        station_info_changed = None
        past_hours_changed = None

        if self.network:
            station_info_changed = (
            self.network != settings["network"] or
            self.station != settings["station"] or
            self.location != settings["location"] or
            self.channel != settings["channel"]
        )
        if self.past_hours:
            past_hours_changed = (
            self.past_hours != settings["past_hours"]
        )

        self.network = settings["network"]
        self.station = settings["station"]
        self.location = settings["location"]
        self.channel = settings["channel"]
        self.server_url = settings["server_url"]
        self.past_hours = settings["past_hours"]
        self.start_time = settings["start_time"]
        self.end_time = settings["end_time"]
        self.line_color = settings["line_color"]
        self.npts_to_add = settings["npts_to_add"]
        self.ani_speed = settings["ani_speed"]

        # 更新图表颜色
        if self.plotting :
            self.line.set_color(self.line_color)
            self.ax.set_title(f"Real-time Seismic Data (Past {self.past_hours} Hours)", color='white')
            self.ax.set_xlim(self.start_time.timestamp, self.end_time.timestamp)
        
        # 如果台站信息有变化，重新下载实时数据
        if station_info_changed:
            self.downloader.update_station_info(
                network=self.network,
                station=self.station,
                location=self.location,
                channel=self.channel
            )
        if self.plotting or station_info_changed or past_hours_changed :
            # 重新下载数据或根据需要更新其他设置
            self.download_initial_data()

    def refrensh_animation(self):
        settings = self.control_panel.get_settings()
        self.update_settings(settings=settings)

    def toggle_animation(self):
        """切换动画的启动和暂停状态"""
        if self.is_animation_running:
            self.ani.event_source.stop()
            self.is_animation_running = False  # 更新标志位
        else:
            self.ani.event_source.start()
            self.is_animation_running = True  # 更新标志位

    def update_past_hours(self):
        self.ax.set_title(f"Real-time Seismic Data (Past {self.past_hours} Hours)", color='white')  # 设置标题颜色
        self.start_time = self.end_time - self.past_hours * 3600

    def download_initial_data(self):
        """下载初始的历史数据"""
        if self.downloader:
            self.downloader.stop_event.clear()
        try:
            print(f"Downloading:{self.network}_{self.station}_{self.location}_{self.channel}")
            stream = Stream()
            stream = self.fdsn_client.get_waveforms(self.network, self.station, self.location, self.channel,
                                                     self.start_time, self.end_time)
            
            if stream:
                stream.merge()
                if self.location == "*":
                    # 如果 location 是 "*", 直接复制整个 stream
                    self.stream_plot = stream.copy()
                else:
                    # 否则，过滤出 location 与 self.location 匹配的 Trace
                    filtered_traces = [tr for tr in stream if tr.stats.location == self.location]
                    if filtered_traces:
                        self.stream_plot = Stream(traces=filtered_traces)
                    else:
                        # 如果没有匹配的 trace，可以选择清空 stream_plot 或者保留之前的数据
                        self.stream_plot = stream.copy()  # 清空，或者你可以选择保留原来的数据

            if self.downloader:
                self.downloader.stop_event.clear()
        except Exception as e:
            print(f"Error downloading initial data: {e}")
    
    def find_matching_trace(self):
        '''
        查找 downloader.stream 中与 stream_plot 具有相同 location 和 channel 的 trace。
        '''
        if not self.stream_plot or len(self.stream_plot) == 0:
            return None  # 如果没有 stream_plot 数据，则返回 None

        # 获取 stream_plot 的 location 和 channel
        reference_trace = self.stream_plot[0]  # 假设我们只关心第一个 stream_plot 的 trace
        target_network = reference_trace.stats.network
        target_station = reference_trace.stats.station
        target_location = reference_trace.stats.location
        target_channel = reference_trace.stats.channel

        # 用于存放匹配的 trace
        matching_traces = Stream()

        if self.downloader.stream:
            for trace in self.downloader.stream:
                if (trace.stats.network == target_network and trace.stats.station == target_station 
                    and trace.stats.location == target_location and trace.stats.channel == target_channel):
                    # 添加匹配的 trace 到 matching_traces
                    matching_traces.append(trace)
                    # 如果找到匹配的 trace，则更新 downloader.stream 并返回匹配的 trace
                    if len(matching_traces) > 0:
                        self.downloader.stream = matching_traces
                        self.downloader.stream.merge()  # 合并相同的 trace
                    return trace  # 返回匹配的 trace

        return None  # 如果没有找到匹配的 trace，则返回 None
    
    def updata_stream_plot(self):
        """
        从 self.stream 中逐步提取数据，更新 self.stream_plot
        """
        try:
            # 锁定 stream 防止其他线程同时修改
            with self.downloader.stream_lock:
                # 确保 self.stream 中有数据可供处理
                if len(self.downloader.stream) > 0:
                    # 每次从 stream 中取出一小段数据（例如取出第一个 Trace 的一部分）
                    trace = self.find_matching_trace()
                    if trace == None:
                        return
                    self.trace = trace.copy()


                    if len(trace.data) > 1:
                        # 检查时间重叠并进行裁剪
                        if len(self.stream_plot[0]) > 0:
                            plot_endtime = self.stream_plot[0].stats.endtime
                            # 将时间转换为 Unix 时间戳，保留到小数点后四位
                            plot_endtime_rounded = round(plot_endtime.timestamp, 4)
                            # 将四舍五入后的时间戳转换回 UTCDateTime 对象
                            plot_endtime = UTCDateTime(plot_endtime_rounded)
                            trace_starttime = trace.stats.starttime
                            trace_starttime_rounded = round(trace_starttime.timestamp,4)
                            trace_starttime = UTCDateTime(trace_starttime_rounded)

                            tolerance = 2e-6  # 2 微秒的容差
                            if ( trace_starttime < plot_endtime and 
                                trace.stats.endtime >= plot_endtime ):
                                if abs((trace_starttime - plot_endtime)) < tolerance:
                                    pass
                                elif trace.stats.endtime != plot_endtime and abs((trace.stats.endtime - plot_endtime)) < tolerance:
                                    trace_new = trace.slice(trace.stats.endtime , trace.stats.endtime)
                                else:
                                    trace_new = trace.slice(plot_endtime , trace.stats.endtime)
                                    self.downloader.stream[0] = trace_new.copy()
                                    trace = self.downloader.stream[0]

                            elif trace_starttime > plot_endtime:
                                self.download_initial_data()

                    if len(trace.data) > 1:
                        # 如果 trace 数据长度大于需要添加的点数
                        if len(trace.data) > self.npts_to_add:
                            # 从 trace 中分离出一小段数据
                            new_data = trace.slice(trace.stats.starttime, 
                                                trace.stats.starttime + self.npts_to_add * trace.stats.delta)
                            # 更新 self.stream_plot
                            self.stream_plot[0] += new_data.copy()
                            # 将已处理的数据从 self.stream 中移除
                            trace_new = trace.slice(trace.stats.starttime + 
                                                        self.npts_to_add * trace.stats.delta, trace.stats.endtime)    
                            self.downloader.stream[0] = trace_new.copy()
                        else:
                            # 如果剩余的数据点不足 npts_to_add，直接全部添加到 stream_plot
                            new_trace = Trace(data=trace.data.copy(), header=trace.stats)
                            self.stream_plot[0] += new_trace
                            trace_new = trace.slice(trace.stats.endtime, trace.stats.endtime)
                            self.downloader.stream[0] = trace_new.copy()

        except Exception as e:
            error_msg = f"Error in Updata Stream Plot processing: {e}\n\n{traceback.format_exc()}"
            print("Error",error_msg)

    def update_plot(self, frame):
        """更新图表内容"""
        
        try:
            if not self.is_animation_running:  # 检查动画是否仍在运行
                return []
            if not self.line:
                print("---")
                return []  # 返回一个空列表，表示没有有效的 Artist 对象
            self.plotting = True
            self.updata_stream_plot()
            with self.downloader.stream_lock:
                if len(self.stream_plot) > 0:
                    data = self.stream_plot[0].data
                    times = self.stream_plot[0].times(reftime=self.stream_plot[0].stats.starttime)
                    absolute_times = times + self.stream_plot[0].stats.starttime.timestamp

                    self.line.set_data(absolute_times, data)
                    self.ax.set_ylim(min(data), max(data))

                    current_time = UTCDateTime().timestamp
                    start_time = current_time - self.past_hours * 3600
                    self.ax.set_xlim(start_time, current_time)

                    self.ax.relim()
                    self.ax.autoscale_view()

                    if self.trace:
                        # 添加信息显示区域
                        info_text = (f"Network: {self.trace.stats.network}\nStation: {self.trace.stats.station}\n"
                                    f"Location: {self.trace.stats.location}\nChannel: {self.trace.stats.channel}")
                    else:
                        # 添加信息显示区域
                        info_text = (f"Network: {self.network}\nStation: {self.station}\n"
                                    f"Location: {self.location}\nChannel: {self.channel}")
                        # 在更新时修改文本内容
                    self.text_artist.set_text(info_text)


                    # text_artist  = self.ax.text(0.99, 0.95, info_text, transform=self.ax.transAxes,
                    #                 fontsize=10, verticalalignment='top', horizontalalignment='left',
                    #                 bbox=dict(facecolor='white', alpha=0.5))

                    # 检查显示异常
                    thresholds = start_time + 0.1 * 3600 * 0.25
                    if len(data) == 0 or max(absolute_times) < thresholds :
                        print("Low data available for the current time range, refreshing animation...")
                        self.low_data_num += 1
                        if self.low_data_num > 5 and self.past_hours < 0.05:
                            self.control_panel.past_hours_input.setText("0.05")
                            self.low_data_num = 0
                        if self.low_data_num > 6 and self.past_hours < 0.1:
                            self.control_panel.past_hours_input.setText("0.1")
                        self.refrensh_animation()
                        
            self.canvas.figure.tight_layout()
            self.canvas.draw()

            # 检查 self.line 是否是 Artist 对象
            if isinstance(self.line, Artist):
                return self.line,
            else:
                print("self.line is not an Artist object!")
                return []
    
        except Exception as e:
            error_msg = f"Error in Updata Plot processing: {e}\n\n{traceback.format_exc()}"
            print("Error",error_msg)
            return []  # 在异常情况下，返回一个空列表以避免错误
        
    def custom_xaxis_formatter(self, x, pos):
        """自定义 x 轴刻度格式"""
        utc_time = UTCDateTime(x)
        if pos == 0:  # 第一个刻度显示日期+时间
            return utc_time.strftime('%Y-%m-%d %H:%M:%S')
        elif utc_time.hour == 0 and utc_time.minute == 0 and utc_time.second == 0:  # 每天的第一个刻度显示日期+时间
            return utc_time.strftime('%Y-%m-%d %H:%M:%S')
        else:  # 当天其他时间只显示时间
            return utc_time.strftime('%H:%M:%S')

    def show_auto_close_message(self, title, message, timeout=2000):
        """
        显示自动关闭的QMessageBox
        :param title: 弹窗标题
        :param message: 显示的消息
        :param timeout: 自动关闭的时间（毫秒）
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        # 启动定时器，在指定时间后关闭消息框
        timer = QTimer(self)
        timer.timeout.connect(msg_box.close)
        timer.start(timeout)

        # 显示消息框，不阻塞
        msg_box.show()

        # 允许程序继续运行而不等待消息框关闭
        return msg_box
    
    def get_station_coordinates(self):
        client = FDSNClient("IRIS")  # 使用 IRIS FDSN 服务
        inventory = client.get_stations(network=self.network, station=self.station, level="station")
        station_info = inventory[0][0]  # 获取第一个台站信息
        latitude = station_info.latitude
        longitude = station_info.longitude
        return latitude, longitude
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Seismic Data Viewer")
        self.screen = QApplication.primaryScreen()
        self.setGeometry(0, 100, self.screen.size().width(), 500)
        # 获取脚本所在目录
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.setWindowIcon(QIcon(os.path.join(self.script_dir, 'icons','SeisD.png')))
        logging.basicConfig(level=logging.DEBUG)
        
        # 创建控制面板
        self.control_panel = ControlPanel(self)

        # 创建 RealTimeSeismicPlotter 并将其嵌入到主窗口中
        self.plotter = RealTimeSeismicPlotter(self, control_panel=self.control_panel)
        # except Exception as e:
            # QMessageBox.critical(self,"Error",f"error in MainWindow processing:{e}")

        # 设置主布局
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.control_panel)
        main_layout.addWidget(self.plotter)
        self.control_panel.setMinimumWidth(200)
        self.control_panel.setMaximumWidth(400)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 设置字体
        font = QFont()
        font.setFamily("Consolas") 
        font.setPointSize(11)
        central_widget.setFont(font)

    def closeEvent(self,event):
        self.on_closing(event)
    
    def on_closing(self,event=None):
        # 创建一个消息框
        reply = QMessageBox(self)
        reply.setWindowTitle('Quit')
        reply.setText('Do you want to quit?')
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply.setDefaultButton(QMessageBox.No)
        
        # 设置消息框的样式
        reply.setStyleSheet(f"""
            QMessageBox {{
                background-color: white;
                color: black;
            }}
            QMessageBox QLabel {{
                background-color: white;
                color: black;
            }}
            QPushButton {{
                background-color: white;
                color: black;
            }}
        """)
        
        # 显示消息框并获取用户选择
        result = reply.exec_()
        if result == QMessageBox.Yes:
            self.plotter.stop_all_operations()
            QApplication.instance().quit()
        else:
            event.ignore()  # 阻止默认的关闭行为

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
