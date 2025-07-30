import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton, QLabel, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.core.stream import Stream
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class SeismicPlotter(QWidget):
    def __init__(self, parent=None):
        super(SeismicPlotter, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Create main layout
        main_layout = QHBoxLayout(self)

        # Create left panel for controls
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        self.start_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_time_edit.setCalendarPopup(True)
        self.start_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        control_layout.addWidget(QLabel("Start Time:"))
        control_layout.addWidget(self.start_time_edit)

        self.end_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_time_edit.setCalendarPopup(True)
        self.end_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        control_layout.addWidget(QLabel("End Time:"))
        control_layout.addWidget(self.end_time_edit)

        self.download_button = QPushButton("Download and Plot")
        self.download_button.clicked.connect(self.download_and_plot)
        control_layout.addWidget(self.download_button)
        control_layout.addStretch()

        # Create right panel for plotting
        self.plot_widget = QWidget()
        plot_layout = QVBoxLayout(self.plot_widget)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas)

        # Add widgets to main splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(control_panel)
        self.splitter.addWidget(self.plot_widget)

        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)

    def download_and_plot(self):
        start_time = self.start_time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        end_time = self.end_time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        # Convert to UTCDateTime format
        start_time_utc = UTCDateTime(start_time)
        end_time_utc = UTCDateTime(end_time)

        # Download seismic data
        client = Client("IRIS")
        st= Stream()
        try:
            st = client.get_waveforms(network="IU", station="ANMO", location="*",
                                      channel="BHZ", starttime=start_time_utc,
                                      endtime=end_time_utc)
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

        # Clear the previous plot
        # self.ax.clear()
        print(st)
        # Plot the seismic data
        st.plot()
        
        # Refresh the canvas
        # self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = SeismicPlotter()
    window.setWindowTitle('Seismic Data Downloader and Plotter')
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
