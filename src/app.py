from generated.random_toolbox_main_window import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QStandardItem
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import statsmodels.api as sm
import sys
import os
import time
from optical_chaos_rng_sim.random_toolbox import load_bit_sequence, parse_bit_sequence, pack_bits

from bitarray import bitarray


class RandomToolboxMainWindow(QMainWindow, Ui_RandomToolboxMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.seq_bytes = b''

        self.figure = plt.figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)

        self.pushButton_OpenFile.clicked.connect(self.open_file)
        self.pushButton_PlotTimeSeries.clicked.connect(self.plot_time_series)
        self.pushButton_PlotHistogram.clicked.connect(self.plot_histogram)
        self.pushButton_PlotPsd.clicked.connect(self.plot_psd)
        self.pushButton_PlotAcf.clicked.connect(self.plot_acf)

    def open_file(self):
        file, success = QFileDialog.getOpenFileName(
            self, 'Open Bit Sequence File', '', 'Binary files (*.bin *.txt)')
        if success:
            self.seq_bytes = load_bit_sequence(file)

    def plot_time_series(self):
        bit_width = self.spinBox_BitWidth.value()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_ylim(0, 2**bit_width-1)
        ax.set_title('Time Series')
        ax.plot(parse_bit_sequence(self.seq_bytes, bit_width=bit_width))
        self.canvas.draw()

    def plot_histogram(self):
        bit_width = self.spinBox_BitWidth.value()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('Histogram')
        ax.set_xlim(0, 2**bit_width)
        ax.hist(parse_bit_sequence(self.seq_bytes, bit_width=bit_width))
        self.canvas.draw()

    def plot_psd(self):
        bit_width = self.spinBox_BitWidth.value()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('PSD')
        ax.psd(parse_bit_sequence(self.seq_bytes, bit_width=bit_width), NFFT=1024)
        self.canvas.draw()

    def plot_acf(self):
        bit_width = self.spinBox_BitWidth.value()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('ACF')
        ax.plot(sm.tsa.acf(parse_bit_sequence(self.seq_bytes, bit_width=bit_width)))
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = RandomToolboxMainWindow()
    mainWin.show()
    sys.exit(app.exec_())
