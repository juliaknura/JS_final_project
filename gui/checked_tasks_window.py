from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect, QSize, Qt
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options
import sys
from program.Settings import Settings
from program.Tasker import Tasker
from program.Task import Task
import os
from gui.add_task_window import AddTaskWindow
from gui.action_menu_window import ActionMenuWindow


class CheckedTasksWindow(QWidget):
    def __init__(self, parent, tasker, settings):
        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings

        # hide parent window
        self.parent_widget.hide()

        # language settings
        self.language_setting = self.settings.language_option
        # self.language_setting = "silly"
        self.language_dict = language_options[self.language_setting]
        # TODO - to pewnie lepiej bedzie potem wyszczegolnic do funkcji

        # main window properties
        self.setWindowTitle(self.language_dict["checked_tasks_window_title"])
        self.setGeometry(100, 100, 940, 800)

        # widgets
        self.main_widget = QWidget()
        self.top_actions_widget = QWidget()
        self.top_actions_widget.setFixedSize(940, 75)
        self.date_widget = QWidget()
        self.date_widget.setFixedSize(940, 40)
        self.central_content_widget = QWidget()
        self.task_list_widget = QWidget()
        self.detail_widget = QWidget()
        self.task_details_widget = QWidget()
        self.task_actions_widget = QWidget()

        self.left_buttons_widget = QWidget()
        self.left_buttons_widget.setFixedSize(200, 50)
        self.right_buttons_widget = QWidget()
        self.right_buttons_widget.setFixedSize(350, 60)

        # layouts
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_actions_layout = QHBoxLayout()
        self.top_actions_widget.setLayout(self.top_actions_layout)

        self.date_layout = QHBoxLayout()
        self.date_widget.setLayout(self.date_layout)

        self.central_content_layout = QHBoxLayout()
        self.central_content_widget.setLayout(self.central_content_layout)

        self.task_list_layout = QHBoxLayout()
        self.task_list_widget.setLayout(self.task_list_layout)

        self.detail_layout = QVBoxLayout()
        self.detail_widget.setLayout(self.detail_layout)

        self.task_details_layout = QVBoxLayout()
        self.task_details_widget.setLayout(self.task_details_layout)

        self.task_actions_layout = QHBoxLayout()
        self.task_actions_widget.setLayout(self.task_actions_layout)

        self.left_buttons_layout = QHBoxLayout()
        self.left_buttons_widget.setLayout(self.left_buttons_layout)

        self.right_buttons_layout = QHBoxLayout()
        self.right_buttons_widget.setLayout(self.right_buttons_layout)


        # buttons
        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])
        self.action_menu_button = QPushButton()
        self.action_menu_button.setText(self.language_dict["action_menu_button"])
        self.action_menu_button.setFixedSize(170, 50)
        self.add_task_button = QPushButton()
        self.add_task_button.setIcon(QIcon(os.getcwd() + os.sep + "gui" + os.sep + "plus_icon.png"))
        self.add_task_button.setIconSize(QSize(40, 40))
        self.add_task_button.setFixedSize(50, 50)
        self.add_task_button.show()
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(os.getcwd() + os.sep + "gui" + os.sep + "settings.png"))
        self.settings_button.setIconSize(QSize(40, 40))
        self.settings_button.setFixedSize(50, 50)
        self.settings_button.show()
        self.template_button = QPushButton()
        self.template_button.setText(self.language_dict["template_button"])
        self.choose_date_button = QPushButton()
        self.choose_date_button.setText(self.language_dict["choose_date_button"])


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
        self.date_field = QDateEdit()

        # spacer
        self.spacer = QSpacerItem(400, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # checkbox widgets
        self.task_list = CheckBoxListWidget()
        self.subtask_list = CheckBoxListWidget()

        # text labels
        self.task_name_label = QLabel(self.language_dict["task_name_label"])
        self.task_desc_label = QLabel(self.language_dict["task_desc_label"])
        self.task_deadline_label = QLabel(self.language_dict["task_deadline_label"])
        self.task_exec_date_label = QLabel(self.language_dict["task_exec_date_label"])
        self.subtasks_label = QLabel(self.language_dict["subtasks_label"])
        self.date_label = QLabel(self.language_dict["date_label"])
        self.task_cat_label = QLabel(self.language_dict["task_cat_label"])

        # arrange main window
        self.self_layout = QHBoxLayout()
        self.self_layout.addWidget(self.main_widget)
        self.setLayout(self.self_layout)

        # arrange main widget
        self.main_layout.addWidget(self.top_actions_widget)
        self.main_layout.addWidget(self.date_widget)
        self.main_layout.addWidget(self.central_content_widget)

        # arrange top actions widget
        self.top_actions_layout.addWidget(self.left_buttons_widget, alignment=Qt.AlignLeft)
        self.top_actions_layout.addWidget(self.right_buttons_widget, alignment=Qt.AlignRight)

        # arrange left buttons
        self.left_buttons_layout.addWidget(self.back_button)

        # arrange right buttons
        self.right_buttons_layout.addWidget(self.action_menu_button)
        self.right_buttons_layout.addWidget(self.settings_button)
        self.right_buttons_layout.addWidget(self.add_task_button)

        # arrange date widget
        self.date_layout.addWidget(self.date_label)
        self.date_layout.addWidget(self.date_field)
        self.date_layout.addWidget(self.choose_date_button)
        self.date_layout.addItem(self.spacer)


        # arrange central content widget
        self.central_content_layout.addWidget(self.task_list_widget)
        self.central_content_layout.addWidget(self.detail_widget)

        # arrange task list widget
        self.task_list_layout.addWidget(self.task_list)

        # arrange detail widget
        self.detail_layout.addWidget(self.task_details_widget)
        self.detail_layout.addWidget(self.task_actions_widget)


        # arrange task det widget
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

        # arrange task actions widget
        self.task_actions_layout.addWidget(self.template_button, alignment=Qt.AlignCenter)

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)
        self.add_task_button.clicked.connect(self.add_task_window_show)
        self.action_menu_button.clicked.connect(self.action_menu_window_show)

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

    def add_task_window_show(self):
        self.add_task_window = AddTaskWindow(self, self.tasker, self.settings, None)
        self.add_task_window.show()

    def action_menu_window_show(self):
        self.action_menu_window = ActionMenuWindow(self, self.tasker, self.settings)
        self.action_menu_window.show()

    def update_window(self):
        print("checked tasks window updated")