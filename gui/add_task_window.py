from typing import Optional

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

class AddTaskWindow(QWidget):

    def __init__(self, parent, tasker, settings, template_task: Optional[Task]):

        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings
        self.template_task = template_task
        self.categories_list = self.get_category_list()

        # hide parent window
        self.parent_widget.hide()

        # language settings
        self.language_setting = self.settings.language_option
        # self.language_setting = "silly"
        self.language_dict = language_options[self.language_setting]
        # TODO - to pewnie lepiej bedzie potem wyszczegolnic do funkcji


        # main window properties
        self.setWindowTitle(self.language_dict["add_tasks_window_title"])
        self.setGeometry(100, 100, 450, 800)

        # widgets
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.top_widget.setFixedSize(450, 60)
        self.content_widget = QWidget()
        self.deadline_widget = QWidget()
        self.exec_date_widget = QWidget()
        self.subtasks_button_widget = QWidget()

        # layouts
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        self.deadline_layout = QHBoxLayout()
        self.deadline_widget.setLayout(self.deadline_layout)

        self.exec_date_layout = QHBoxLayout()
        self.exec_date_widget.setLayout(self.exec_date_layout)

        self.subtasks_button_layout = QHBoxLayout()
        self.subtasks_button_widget.setLayout(self.subtasks_button_layout)


        # buttons
        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])
        self.add_button = QPushButton()
        self.add_button.setText(self.language_dict["add_tasks_window_title"])
        self.new_subtask_button = QPushButton()
        self.new_subtask_button.setText(self.language_dict["new_subtask_button"])
        self.delete_subtask_button = QPushButton()
        self.delete_subtask_button.setText(self.language_dict["delete_subtask_button"])
        self.none_deadline = QRadioButton()
        self.none_deadline.setText(self.language_dict["none_button"])
        self.none_exec_date = QRadioButton()
        self.none_exec_date.setText(self.language_dict["none_button"])


        # labels
        self.top_title_add_window = QLabel(self.language_dict["top_title_add_window"])
        font = self.top_title_add_window.font()
        font.setBold(True)
        font.setPointSize(20)
        self.top_title_add_window.setFont(font)
        self.task_name_label = QLabel(self.language_dict["task_name_label"])
        self.task_cat_label = QLabel(self.language_dict["task_cat_label"])
        self.task_desc_label = QLabel(self.language_dict["task_desc_label"])
        self.task_deadline_label = QLabel(self.language_dict["task_deadline_label"])
        self.task_exec_date_label = QLabel(self.language_dict["task_exec_date_label"])
        self.subtasks_label = QLabel(self.language_dict["subtasks_label"])

        # fields
        self.name_field = QLineEdit()
        self.desc_field = QLineEdit()
        self.deadline_field = QDateEdit()
        self.exec_date_field = QDateEdit()

        # checkbox lists
        self.subtask_list = QListWidget()

        # combo box
        self.category_combo_box = QComboBox()
        self.category_combo_box.addItems(self.categories_list)

        # spacer
        self.spacer = QSpacerItem(100, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

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
        self.top_layout.addWidget(self.top_title_add_window)

        # arrange content widget
        self.content_layout.addWidget(self.task_name_label)
        self.content_layout.addWidget(self.name_field)
        self.content_layout.addWidget(self.task_cat_label)
        self.content_layout.addWidget(self.category_combo_box)
        self.content_layout.addWidget(self.task_desc_label)
        self.content_layout.addWidget(self.desc_field)
        self.content_layout.addWidget(self.task_deadline_label)
        self.content_layout.addWidget(self.deadline_widget)
        self.content_layout.addWidget(self.task_exec_date_label)
        self.content_layout.addWidget(self.exec_date_widget)
        self.content_layout.addWidget(self.subtasks_label)
        self.content_layout.addWidget(self.subtask_list)
        self.content_layout.addWidget(self.subtasks_button_widget)
        self.content_layout.addWidget(self.add_button)

        # arrange subtask button widget
        self.subtasks_button_layout.addWidget(self.new_subtask_button)
        self.subtasks_button_layout.addWidget(self.delete_subtask_button)

        # arrange deadline widget
        self.deadline_layout.addWidget(self.deadline_field)
        self.deadline_layout.addWidget(self.none_deadline)

        # arrange exec desc widget
        self.exec_date_layout.addWidget(self.exec_date_field)
        self.exec_date_layout.addWidget(self.none_exec_date)

        self.back_button.clicked.connect(self.back_to_main_window)



    def get_category_list(self):
        return ["kat1", "kat2", "kat3"]


    def fill_from_template(self):
        if self.template_task is not None:
            ...

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()