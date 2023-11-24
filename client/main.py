import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, \
    QTimeEdit, QDialog, QDialogButtonBox
from login import LoginWindow
from client import ClientThread
from th_graph import PlotWindow
from link_serial import *
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
