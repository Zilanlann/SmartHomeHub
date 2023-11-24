import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class PlotWindow(QMainWindow):

    def __init__(self, combined_data):
        super().__init__()

        # 解析传入的字符串
        str_hour, str_temperature, str_humidity = combined_data.split('|')
        hour = self.extract_array(str_hour)
        temperature = self.extract_array(str_temperature)
        humidity = self.extract_array(str_humidity)

        # 创建绘图控件
        self.plotWidget = pg.PlotWidget()

        # 添加温度数据线
        self.plotWidget.plot(hour, temperature, pen='r', name='Temperature')

        # 添加湿度数据线
        self.plotWidget.plot(hour, humidity, pen='b', name='Humidity')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.plotWidget)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

    @staticmethod
    def extract_array(str_data):
        str_array = str_data.split('=')[1].strip()
        return eval(str_array)

