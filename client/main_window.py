import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, \
    QDialog

from change_pass import ChangePasswordDialog
from client import ClientThread
from face_recognize import FaceThread
from link_serial import SerialThread
from th_graph import PlotWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.status = 0
        self.client_thread = ClientThread()
        self.client_thread.start()
        self.client_thread.received_message.connect(self.switchFunc)
        self.face_thread = FaceThread()
        self.face_thread.isOwner.connect(self.checkFace)
        self.serial_thread = SerialThread('COM9', 9600)
        self.serial_thread.received_data_signal.connect(self.sendTemp)

    def initUI(self):
        self.setWindowTitle('智能家居管理系统')
        self.resize(400, 300)

        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 布局
        layout = QVBoxLayout(central_widget)

        # 系统标题
        title = QLabel('智能家居管理系统')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 居中对齐
        title.setStyleSheet("font-size: 20px;")  # 设置字体大小
        layout.addWidget(title)

        # 修改密码按钮
        self.change_password_button = QPushButton('修改密码')
        self.change_password_button.clicked.connect(self.change_password)
        layout.addWidget(self.change_password_button)

        # 查看当天温湿度曲线按钮
        self.view_temp_humidity_button = QPushButton('查看24小时温湿度曲线')
        self.view_temp_humidity_button.clicked.connect(self.view_temp_humidity)
        layout.addWidget(self.view_temp_humidity_button)

        # 人脸识别门禁按钮
        self.face_recognition_button = QPushButton('人脸识别门禁')
        self.face_recognition_button.clicked.connect(self.face_recognition)
        layout.addWidget(self.face_recognition_button)

    def closeEvent(self, event):
        self.client_thread.clean_up()
        event.accept()

    def switchFunc(self, message):
        # 处理接收到的消息
        if self.status == 1:
            result = int(message)
            if result == 1:
                QMessageBox.information(self, '提示', "密码修改成功")
            elif result == 0:
                QMessageBox.warning(self, '错误', '旧密码错误！')
            else:
                QMessageBox.warning(self, '错误', '用户不存在！')
        elif self.status == 2:
            self.plot_window = PlotWindow(message)
            self.plot_window.show()

    def sendTemp(self, message):
        self.client_thread.send(message)

    def checkFace(self, result):
        if result == 1:
            QMessageBox.information(self, '提示', "门已开，欢迎回家！")
        else:
            QMessageBox.warning(self, '错误', '人脸识别失败')

    def change_password(self):
        self.status = 1
        dialog = ChangePasswordDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, old_password, new_password = dialog.get_inputs()
            self.client_thread.send("changePassword:" + username + "," + old_password + "," + new_password)

    def view_temp_humidity(self):
        self.status = 2
        self.client_thread.send("getTH")

    def face_recognition(self):
        self.status = 3
        self.face_thread.start()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
