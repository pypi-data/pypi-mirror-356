import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from obspy.clients.seedlink.easyseedlink import create_client
from obspy.clients.fdsn import Client as FDSNClient
from obspy import Stream, UTCDateTime
from ..seisd_main import CustomDateFormatter

class RealTimeSeismicPlotter(QWidget):
    def __init__(self, parent=None, network="IU", station="ANMO", location="*", channel="BHZ", 
                 server_url="rtserve.iris.washington.edu", past_hours=0.1, canvas=None):
        super().__init__(parent)

        self.network = network
        self.station = station
        self.location = location
        self.channel = channel
        self.server_url = server_url
        self.past_hours = past_hours
        self.stream = Stream()
        self.stream_lock = threading.Lock()

        # 初始化 Matplotlib 图表
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_title(f"Real-time Seismic Data (Past {self.past_hours} Hours)")
        self.ax.set_xlabel("Time (UTC)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)

        # 如果未提供 canvas，则创建一个新的 FigureCanvasQTAgg
        if canvas is None:
            self.canvas = FigureCanvas(self.fig)
            layout = QVBoxLayout()
            layout.addWidget(self.canvas)
            self.setLayout(layout)
        else:
            self.canvas = canvas
            self.canvas.figure = self.fig

        # 初始化时间范围
        self.end_time = UTCDateTime()
        self.start_time = self.end_time - past_hours * 3600
        self.ax.set_xlim(self.start_time.timestamp, self.end_time.timestamp)

        # 下载过去的数据
        self.download_initial_data()

        # 创建并启动后台线程进行数据下载
        self.seedlink_client = create_client(self.server_url, on_data=lambda trace: self.handle_data(trace))
        self.seedlink_client.select_stream(self.network, self.station, self.channel)
        self.download_thread = threading.Thread(target=self.download_data)
        self.download_thread.daemon = True
        self.download_thread.start()

        # 启动动画
        self.ani = FuncAnimation(self.fig, self.update_plot, blit=True, interval=1000, cache_frame_data=False)

    def download_initial_data(self):
        """下载初始的历史数据"""
        fdsn_client = FDSNClient("IRIS")
        try:
            self.stream = fdsn_client.get_waveforms(self.network, self.station, self.location, self.channel, self.start_time, self.end_time)
        except Exception as e:
            print(f"Error downloading initial data: {e}")

    def handle_data(self, trace):
        """处理实时到达的数据"""
        with self.stream_lock:
            self.stream += trace
            self.stream.merge()

    def download_data(self):
        """启动 SeedLink 客户端接收实时数据"""
        self.seedlink_client.run()

    def update_plot(self, frame):
        """更新图表内容"""
        with self.stream_lock:
            if len(self.stream) > 0:
                data = self.stream[-1].data
                times = self.stream[-1].times(reftime=self.stream[-1].stats.starttime)
                absolute_times = times + self.stream[-1].stats.starttime.timestamp

                self.line.set_data(absolute_times, data)
                self.ax.set_ylim(min(data), max(data))
                self.ax.xaxis.set_major_formatter(CustomDateFormatter('%Y-%m-%d %H:%M:%S', '%H:%M'))
                current_time = UTCDateTime().timestamp
                starttime = current_time - self.past_hours * 3600

                self.ax.set_xlim(starttime, current_time)

                self.ax.relim()
                self.ax.autoscale_view()

        self.canvas.draw()
        return self.line,

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Seismic Data Viewer")

        # 创建 RealTimeSeismicPlotter 并将其嵌入到主窗口中
        self.plotter = RealTimeSeismicPlotter(self)
        self.setCentralWidget(self.plotter)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
