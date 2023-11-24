from PyQt6.QtWidgets import QLineEdit, QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('修改密码')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 用户名
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('用户名')
        layout.addWidget(self.username_edit)

        # 旧密码
        self.old_password_edit = QLineEdit()
        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_password_edit.setPlaceholderText('旧密码')
        layout.addWidget(self.old_password_edit)

        # 新密码
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_edit.setPlaceholderText('新密码')
        layout.addWidget(self.new_password_edit)

        # 按钮
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_inputs(self):
        return self.username_edit.text(), self.old_password_edit.text(), self.new_password_edit.text()
