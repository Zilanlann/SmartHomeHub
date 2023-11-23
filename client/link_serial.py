import threading

import serial


class ComClass:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.comSerial = None
        self.run = False
        self.open()

    def start_threads(self):
        """启动线程"""
        self.thread1 = threading.Thread(target=self.receiveData)
        self.thread2 = threading.Thread(target=self.sendData)
        self.thread1.start()
        self.thread2.start()
        self.thread1.join()
        self.thread2.join()
        ser.close()

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

    def sendData(self, send_data=''):
        """发送数据"""
        if send_data:
            self.comSerial.write(send_data.encode('UTF-8'))
            print('发送数据：%s' % send_data)

    def receiveData(self):
        """接收数据"""
        while self.run:
            if self.comSerial.inWaiting() > 0:
                receive_data = self.comSerial.readline().decode('ascii')
                if receive_data:
                    print('接收数据：%s' % receive_data)


if __name__ == '__main__':
    ser = ComClass('COM9', 9600)
    ser.start_threads()
