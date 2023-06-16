from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QComboBox, QRadioButton, QListWidget, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect, QSize, Qt
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options
import sys
from program.Settings import Settings
from program.Tasker import Tasker
from program.Task import Task
import os


class ManageCategoriesWindow(QWidget):

    def __init__(self, parent, tasker, settings):
        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings
        self.category_list = self.get_categories()

        # hide parent window
        self.parent_widget.hide()

        # language settings
        self.language_setting = self.settings.language_option
        # self.language_setting = "silly"
        self.language_dict = language_options[self.language_setting]
        # TODO - to pewnie lepiej bedzie potem wyszczegolnic do funkcji

        # main window properties
        self.setWindowTitle(self.language_dict["cat_label"])
        self.setGeometry(100, 100, 550, 400)

        # widgets
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.top_widget.setFixedSize(550, 50)
        self.content_widget = QWidget()
        self.button_widget = QWidget()

        # layouts
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        self.button_layout = QHBoxLayout()
        self.button_widget.setLayout(self.button_layout)

        # buttons
        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])
        self.add_category_button = QPushButton()
        self.add_category_button.setText(self.language_dict["add_category_button"])
        self.delete_category_button = QPushButton()
        self.delete_category_button.setText(self.language_dict["delete_category_button"])

        # list widget
        self.cat_list_widget = QListWidget()
        self.cat_list_widget.addItems(self.category_list)

        # label
        self.title_label = QLabel(self.language_dict["category_window_title"])
        font = self.title_label.font()
        font.setBold(True)
        font.setPointSize(20)
        self.title_label.setFont(font)

        # spacer
        self.spacer = QSpacerItem(80, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # arrange main window
        self.self_layout = QHBoxLayout()
        self.self_layout.addWidget(self.main_widget)
        self.setLayout(self.self_layout)

        # arrange main widget
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.addWidget(self.content_widget)

        # arrange top widget
        self.top_layout.addWidget(self.back_button)
        self.top_layout.addItem(self.spacer)
        self.top_layout.addWidget(self.title_label)

        # arrange content widget
        self.content_layout.addWidget(self.cat_list_widget)
        self.content_layout.addWidget(self.button_widget)

        # arrange button widget
        self.button_layout.addWidget(self.add_category_button)
        self.button_layout.addWidget(self.delete_category_button)

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)

    def get_categories(self):
        return ["k1", "k2", "k3"]

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

