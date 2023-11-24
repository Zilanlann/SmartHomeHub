import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class PlotWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # 假设这些是从服务器获取的字符串
        str_hour = "hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        str_temperature = "temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 21]"
        str_humidity = "humidity = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"

        # 解析字符串
        hour = self.extract_array(str_hour)
        temperature = self.extract_array(str_temperature)
        humidity = self.extract_array(str_humidity)

        # 创建一个绘图控件
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


def main():
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
