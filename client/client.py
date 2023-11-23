from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
import socket
import sys


class ClientThread(QThread):
    received_message = pyqtSignal(str)
    connection_error = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('localhost', 12345))
        except socket.error as e:
            print(f"Socket error: {e}")
            self.connection_error.emit()
            return

    def run(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if not message:
                    break
                self.received_message.emit(message)
            except socket.error as e:
                print(f"Socket error: {e}")
                self.connection_error.emit()
                break

    def send(self, message):
        try:
            self.sock.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Socket error: {e}")
            self.connection_error.emit()

    def clean_up(self):
        self.sock.close()


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("客户端")
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.lineEdit = QLineEdit()
        self.pushButton = QPushButton("发送")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.pushButton)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.client_thread = ClientThread()
        self.client_thread.received_message.connect(self.display_message)
        self.client_thread.connection_error.connect(self.on_connection_error)
        self.client_thread.start()

        self.pushButton.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.client_thread.clean_up()
        event.accept()
    def send_message(self):
        message = self.lineEdit.text()
        self.client_thread.send(message)
        self.lineEdit.clear()

    def display_message(self, message):
        self.textEdit.append(message)

    def on_connection_error(self):
        self.textEdit.append("连接错误，请检查服务器状态或网络连接。")
        self.pushButton.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec())
