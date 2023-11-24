import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

from client import ClientThread

from time import sleep

from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client_thread = ClientThread()
        self.client_thread.start()
        self.client_thread.received_message.connect(self.checkLogin)

    def initUI(self):
        self.setWindowTitle('用户登录')

        # 布局
        layout = QVBoxLayout()
        # 用户名
        self.username_label = QLabel('用户名')
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # 密码
        self.password_label = QLabel('密码')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # 登录按钮
        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def closeEvent(self, event):
        self.client_thread.clean_up()
        event.accept()

    def checkLogin(self, message):
        # 处理接收到的消息
        result = int(message)
        if result == 1:
            QMessageBox.information(self, '提示', '登录成功！')
        elif result == 0:
            QMessageBox.warning(self, '错误', '密码错误！')
        else:
            QMessageBox.warning(self, '错误', '用户不存在！')

    def send_message(self, message):
        self.client_thread.send(message)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.send_message("checkLogin:" + username + "," + password)


def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
