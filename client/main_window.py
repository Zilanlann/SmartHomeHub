import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, \
    QTimeEdit, QDialog, QDialogButtonBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        self.view_temp_humidity_button = QPushButton('查看当天温湿度曲线')
        self.view_temp_humidity_button.clicked.connect(self.view_temp_humidity)
        layout.addWidget(self.view_temp_humidity_button)

        # 人脸识别门禁按钮
        self.face_recognition_button = QPushButton('人脸识别门禁')
        self.face_recognition_button.clicked.connect(self.face_recognition)
        layout.addWidget(self.face_recognition_button)

        # # 关灯睡觉按钮
        # self.sleep_button = QPushButton('关灯睡觉')
        # self.sleep_button.clicked.connect(self.set_sleep_time)
        # layout.addWidget(self.sleep_button)

    def change_password(self):
        QMessageBox.information(self, '修改密码', '这里是修改密码的功能')

    def view_temp_humidity(self):
        QMessageBox.information(self, '温湿度曲线', '这里是查看当天温湿度曲线的功能')

    def face_recognition(self):
        QMessageBox.information(self, '人脸识别门禁', '这里是人脸识别门禁的功能')

    def set_sleep_time(self):
        # 弹出对话框设置睡觉时间
        dialog = QDialog(self)
        dialog.setWindowTitle('设置起床时间')

        dialog_layout = QVBoxLayout()

        self.time_edit = QTimeEdit(dialog)
        self.time_edit.setDisplayFormat('HH:mm')
        dialog_layout.addWidget(self.time_edit)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            wakeup_time = self.time_edit.time().toString('HH:mm')
            QMessageBox.information(self, '设置成功', f'明早起床时间设为 {wakeup_time}')


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
