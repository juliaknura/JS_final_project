from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtGui
from program.language_options import language_options
import os


class CatWindow(QWidget):

    def __init__(self, parent, tasker, settings):

        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings

        # hide parent window
        self.parent_widget.hide()

        # language settings
        self.language_setting = self.settings.language_option
        self.language_dict = language_options[self.language_setting]

        # main window properties
        self.setWindowTitle(self.language_dict["real_cat_label"])
        self.setGeometry(100, 100, 660, 400)

        # widgets
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.cat_widget = QWidget()

        # layouts
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_layout = QVBoxLayout()
        self.top_widget.setLayout(self.top_layout)

        self.cat_layout = QVBoxLayout()
        self.cat_widget.setLayout(self.cat_layout)

        # button
        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])
        self.back_button.setFixedSize(100,25)

        # pixmap
        logo_pixMap = QPixmap(os.getcwd() + os.sep + "gui" + os.sep + "cat.jpg")

        # logo
        self.logo_label = QLabel()
        self.logo_label.setGeometry(QRect(0, 0, 652, 367))
        self.logo_label.setPixmap(logo_pixMap)
        self.logo_label.show()

        # arrange main window
        self.self_layout = QHBoxLayout()
        self.self_layout.addWidget(self.main_widget)
        self.setLayout(self.self_layout)

        # arrange main widget
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.addWidget(self.cat_widget)

        # arrange top widget
        self.top_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # arrange cat widget
        self.cat_layout.addWidget(self.logo_label)

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)

    def back_to_main_window(self):
        self.parent_widget.show()
        self.hide()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_to_main_window()
        a0.ignore()


