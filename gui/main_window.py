from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect, QSize, Qt
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options
import sys
from program.Settings import Settings
from program.Tasker import Tasker
from program.Task import Task
import os


class MainWindow(QMainWindow):

    def __init__(self, mw_tasker, mw_settings):
        super().__init__()

        self.tasker = mw_tasker
        self.settings = mw_settings

        # language settings
        # self.language_setting = self.settings.language_option
        self.language_setting = "polish"
        self.language_dict = language_options[self.language_setting]
        # TODO - to pewnie lepiej bedzie potem wyszczegolnic do funkcji

        # main window properties
        self.setWindowTitle(self.language_dict["main_window_title"])
        self.setGeometry(100, 100, 940, 800)

        # widgets
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.logo_widget = QWidget()
        self.options_widget = QWidget()
        self.top_options_widget = QWidget()
        self.bottom_options_widget = QWidget()
        self.central_widget = QWidget()
        self.central_content_widget = QWidget()
        self.central_title_widget = QWidget()
        self.task_list_widget = QWidget()
        self.detail_widget = QWidget()
        self.task_details_widget = QWidget()
        self.task_actions_widget = QWidget()

        # layouts
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.logo_layout = QVBoxLayout()
        self.options_layout = QVBoxLayout()
        self.top_options_layout = QHBoxLayout()
        self.bottom_options_layout = QHBoxLayout()
        self.central_layout = QVBoxLayout()
        self.central_content_layout = QHBoxLayout()
        self.central_title_layout = QVBoxLayout()
        self.task_list_layout = QHBoxLayout()
        self.detail_layout = QVBoxLayout()
        self.task_details_layout = QVBoxLayout()
        self.task_actions_layout = QHBoxLayout()

        # text labels
        self.task_name_label = QLabel(self.language_dict["task_name_label"])
        self.task_cat_label = QLabel(self.language_dict["task_cat_label"])
        self.task_desc_label = QLabel(self.language_dict["task_desc_label"])
        self.task_deadline_label = QLabel(self.language_dict["task_deadline_label"])
        self.task_exec_date_label = QLabel(self.language_dict["task_exec_date_label"])
        self.subtasks_label = QLabel(self.language_dict["subtasks_label"])
        self.daily_title_label = QLabel(self.language_dict["daily_title_label"])
        font = self.daily_title_label.font()
        font.setBold(True)
        font.setPointSize(20)
        self.daily_title_label.setFont(font)

        # images
        logo_pixMap = QPixmap(os.getcwd()+os.sep+"gui"+os.sep+"task_manager.png")

        # logo
        self.logo_label = QLabel()
        self.logo_label.setGeometry(QRect(0, 0, 470, 201))
        self.logo_label.setPixmap(logo_pixMap)
        self.logo_label.show()

        # buttons
        self.action_menu_button = QPushButton()
        self.action_menu_button.setText(self.language_dict["action_menu_button"])
        self.action_menu_button.setFixedSize(180, 80)
        self.all_tasks_button = QPushButton()
        self.all_tasks_button.setText(self.language_dict["all_tasks_button"])
        self.all_tasks_button.setFixedSize(360, 80)
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(os.getcwd()+os.sep+"gui"+os.sep+"settings.png"))
        self.settings_button.setIconSize(QSize(70,70))
        self.settings_button.setFixedSize(80, 80)
        self.settings_button.show()
        self.new_task_button = QPushButton()
        self.new_task_button.setIcon(QIcon(os.getcwd()+os.sep+"gui"+os.sep+"plus_icon.png"))
        self.new_task_button.setIconSize(QSize(70, 70))
        self.new_task_button.setFixedSize(80, 80)
        self.new_task_button.show()
        self.new_subtask_button = QPushButton()
        self.new_subtask_button.setText(self.language_dict["new_subtask_button"])
        self.delete_task_button = QPushButton()
        self.delete_task_button.setText(self.language_dict["delete_task_button"])
        self.delete_subtask_button = QPushButton()
        self.delete_subtask_button.setText(self.language_dict["delete_subtask_button"])

        # text_fields
        self.name_field = QLineEdit()
        self.name_field.setEnabled(False)
        self.cat_field = QLineEdit()
        self.cat_field.setEnabled(False)
        self.desc_field = QLineEdit()
        self.desc_field.setEnabled(False)
        self.deadline_field = QDateEdit()
        self.deadline_field.setEnabled(False)
        self.exec_date_field = QDateEdit()
        self.exec_date_field.setEnabled(False)

        # checkbox widgets
        self.task_list = CheckBoxListWidget()
        self.subtask_list = CheckBoxListWidget()

        # arrange main window
        self.setCentralWidget(self.main_widget)

        # arrange main widget
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.addWidget(self.central_widget)
        self.main_widget.setLayout(self.main_layout)

        # arrange top widget
        self.top_layout.addWidget(self.logo_widget)
        self.top_layout.addWidget(self.options_widget)
        self.top_widget.setLayout(self.top_layout)

        # arrange logo widget
        self.logo_layout.addWidget(self.logo_label)
        self.logo_widget.setLayout(self.logo_layout)

        # arrange options widget
        self.options_layout.addWidget(self.top_options_widget)
        self.options_layout.addWidget(self.bottom_options_widget)
        self.options_widget.setLayout(self.options_layout)

        # arrange top options widget
        self.top_options_layout.addWidget(self.action_menu_button)
        self.top_options_layout.addWidget(self.settings_button)
        self.top_options_layout.addWidget(self.new_task_button)
        self.top_options_widget.setLayout(self.top_options_layout)

        # arrange bottom options widget
        self.bottom_options_layout.addWidget(self.all_tasks_button)
        self.bottom_options_widget.setLayout(self.bottom_options_layout)

        # arrange central widget
        self.central_layout.addWidget(self.central_title_widget)
        self.central_layout.addWidget(self.central_content_widget)
        self.central_widget.setLayout(self.central_layout)

        # arrange central title widget
        self.central_title_layout.addWidget(self.daily_title_label, alignment=Qt.AlignCenter)
        self.central_title_widget.setLayout(self.central_title_layout)

        # arrange central content widget
        self.central_content_layout.addWidget(self.task_list_widget)
        self.central_content_layout.addWidget(self.detail_widget)
        self.central_content_widget.setLayout(self.central_content_layout)

        # arrange task list widget
        self.task_list_layout.addWidget(self.task_list)
        self.task_list_widget.setLayout(self.task_list_layout)

        # arrange detail widget
        self.detail_layout.addWidget(self.task_details_widget)
        self.detail_layout.addWidget(self.task_actions_widget)
        self.detail_widget.setLayout(self.detail_layout)

        # arrange task details widget
        self.task_details_layout.addWidget(self.task_name_label)
        self.task_details_layout.addWidget(self.name_field)
        self.task_details_layout.addWidget(self.task_cat_label)
        self.task_details_layout.addWidget(self.cat_field)
        self.task_details_layout.addWidget(self.task_desc_label)
        self.task_details_layout.addWidget(self.desc_field)
        self.task_details_layout.addWidget(self.task_deadline_label)
        self.task_details_layout.addWidget(self.deadline_field)
        self.task_details_layout.addWidget(self.task_exec_date_label)
        self.task_details_layout.addWidget(self.exec_date_field)
        self.task_details_layout.addWidget(self.subtasks_label)
        self.task_details_layout.addWidget(self.subtask_list)
        self.task_details_widget.setLayout(self.task_details_layout)

        # arrange task actions widget
        self.task_actions_layout.addWidget(self.new_subtask_button)
        self.task_actions_layout.addWidget(self.delete_subtask_button)
        self.task_actions_layout.addWidget(self.delete_task_button)
        self.task_actions_widget.setLayout(self.task_actions_layout)
