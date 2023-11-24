import serial
from PyQt6.QtCore import QThread, pyqtSignal


class SerialThread(QThread):
    received_data_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, port, baud):
        super().__init__()
        self.port = port
        self.baud = baud
        self.comSerial = None
        self.run = False

    def run(self):
        """重写run方法，用于执行线程的操作"""
        try:
            self.comSerial = serial.Serial(self.port, self.baud)
            self.run = True
            while self.run:
                if self.comSerial.inWaiting() > 0:
                    receive_data = self.comSerial.readline().decode('ascii')
                    if receive_data:
                        self.received_data_signal.emit(receive_data)
        except Exception as e:
            self.error_signal.emit(str(e))

    def stop(self):
        """停止线程运行"""
        self.run = False
        if self.comSerial and self.comSerial.is_open:
            self.comSerial.close()
        self.quit()
        self.wait()

    def sendData(self, send_data=''):
        """发送数据"""
        if send_data and self.comSerial and self.comSerial.is_open:
            self.comSerial.write(send_data.encode('UTF-8'))

    def open(self):
        """打开串口"""
        try:
            self.comSerial = serial.Serial(self.port, self.baud)
            self.run = True
            print("打开串口成功")
        except Exception as e:
            print("打开串口失败：", e)
            self.close()

    def close(self):
        """关闭串口"""
        if self.comSerial and self.comSerial.is_open:
            self.comSerial.close()
            print("关闭串口")
