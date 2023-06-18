from typing import List

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QSpacerItem, QSizePolicy, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5 import QtGui
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options
import sys
from program.Settings import Settings
from program.Tasker import Tasker
from program.Task import Task
import os
from gui.add_task_window import AddTaskWindow
from gui.action_menu_window import ActionMenuWindow
from gui.settings_window import SettingsWindow
from datetime import datetime

code_color_dict = {
    0: "background-color: red",
    1: "background-color: yellow",
    2: "background-color: green",
    3: "background-color: white"
}


class CheckedTasksWindow(QWidget):
    def __init__(self, parent, tasker: Tasker, settings: Settings):
        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings
        self.current_task_list: List[Task] = []
        self.current_task_name_list: List[str] = []
        self.current_task: Task = None
        self.current_subtasks = []
        self.language_setting = None
        self.language_dict = {}

        self.update_settings()



        # hide parent window
        self.parent_widget.hide()

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

        self.deadline_widget = QWidget()
        self.exec_date_widget = QWidget()

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

        self.deadline_layout = QHBoxLayout()
        self.deadline_widget.setLayout(self.deadline_layout)

        self.exec_date_layout = QHBoxLayout()
        self.exec_date_widget.setLayout(self.exec_date_layout)

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

        # checkbox replacement
        self.task_checkbox_button = QPushButton()
        self.task_checkbox_button.setText(self.language_dict["task_checkbox_button"])
        self.subtask_checkbox_button = QPushButton()
        self.subtask_checkbox_button.setText(self.language_dict["subtask_checkbox_button"])

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

        # list widgets
        self.task_list = QListWidget()
        self.subtask_list = QListWidget()

        # text labels
        self.task_name_label = QLabel(self.language_dict["task_name_label"])
        self.task_desc_label = QLabel(self.language_dict["task_desc_label"])
        self.task_deadline_label = QLabel(self.language_dict["task_deadline_label"])
        self.task_exec_date_label = QLabel(self.language_dict["task_exec_date_label"])
        self.subtasks_label = QLabel(self.language_dict["subtasks_label"])
        self.date_label = QLabel(self.language_dict["date_label"])
        self.task_cat_label = QLabel(self.language_dict["task_cat_label"])

        # self.none_label = QLabel(self.language_dict["none_label"])
        # self.none_label2 = QLabel(self.language_dict["none_label"])
        self.none_label = QLabel("")
        self.none_label2 = QLabel("")

        self.task_state_label = QLabel(self.language_dict["false"])
        self.subtask_state_label = QLabel(self.language_dict["false"])

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
        self.task_details_layout.addWidget(self.task_state_label)
        self.task_details_layout.addWidget(self.task_checkbox_button)
        self.task_details_layout.addWidget(self.task_name_label)
        self.task_details_layout.addWidget(self.name_field)
        self.task_details_layout.addWidget(self.task_cat_label)
        self.task_details_layout.addWidget(self.cat_field)
        self.task_details_layout.addWidget(self.task_desc_label)
        self.task_details_layout.addWidget(self.desc_field)
        self.task_details_layout.addWidget(self.task_deadline_label)
        self.task_details_layout.addWidget(self.deadline_widget)
        self.task_details_layout.addWidget(self.task_exec_date_label)
        self.task_details_layout.addWidget(self.exec_date_widget)
        self.task_details_layout.addWidget(self.subtasks_label)
        self.task_details_layout.addWidget(self.subtask_list)
        self.task_details_layout.addWidget(self.subtask_state_label)
        self.task_details_layout.addWidget(self.subtask_checkbox_button)

        # arrange deadline widget
        self.deadline_layout.addWidget(self.deadline_field)
        self.deadline_layout.addWidget(self.none_label)
        self.deadline_widget.setLayout(self.deadline_layout)

        # arrange exec date widget
        self.exec_date_layout.addWidget(self.exec_date_field)
        self.exec_date_layout.addWidget(self.none_label2)
        self.exec_date_widget.setLayout(self.exec_date_layout)

        # arrange task actions widget
        self.task_actions_layout.addWidget(self.template_button, alignment=Qt.AlignCenter)

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)
        self.add_task_button.clicked.connect(self.add_task_window_show)
        self.action_menu_button.clicked.connect(self.action_menu_window_show)
        self.settings_button.clicked.connect(self.settings_window_show)
        self.template_button.clicked.connect(self.choose_as_template)
        self.choose_date_button.clicked.connect(self.choose_date)
        self.task_checkbox_button.clicked.connect(self.task_toggled)
        self.subtask_checkbox_button.clicked.connect(self.subtask_toggled)
        self.task_list.itemClicked.connect(self.task_clicked)
        self.subtask_list.itemClicked.connect(self.subtask_clicked)

        self.set_initial_buttons_and_fields_state()

    def update_settings(self):
        """updates language settings"""
        self.language_setting = self.settings.language_option
        self.language_dict = language_options[self.language_setting]

    def update_text(self):
        """updates all the text displaying in the window in case the language settings have been changed"""
        self.setWindowTitle(self.language_dict["checked_tasks_window_title"])
        self.back_button.setText(self.language_dict["back_button"])
        self.action_menu_button.setText(self.language_dict["action_menu_button"])
        self.template_button.setText(self.language_dict["template_button"])
        self.choose_date_button.setText(self.language_dict["choose_date_button"])
        self.task_name_label.setText(self.language_dict["task_name_label"])
        self.task_desc_label.setText(self.language_dict["task_desc_label"])
        self.task_deadline_label.setText(self.language_dict["task_deadline_label"])
        self.task_exec_date_label.setText(self.language_dict["task_exec_date_label"])
        self.subtasks_label.setText(self.language_dict["subtasks_label"])
        self.date_label.setText(self.language_dict["date_label"])
        self.task_cat_label.setText(self.language_dict["task_cat_label"])
        self.none_label.setText(self.language_dict["none_label"])
        self.none_label2.setText(self.language_dict["none_label"])

        self.task_checkbox_button.setText(self.language_dict["task_checkbox_button"])
        self.subtask_checkbox_button.setText(self.language_dict["subtask_checkbox_button"])
        self.task_state_label.setText(self.language_dict["false"])
        self.subtask_state_label.setText(self.language_dict["false"])

    def pull_task_list(self, chosen_date):
        print("dupa enter pull task list function")
        # pull task list
        self.tasker.get_by_checked_off_date(chosen_date)
        self.current_task_list = self.tasker.get_current_list()
        self.current_task = None
        self.current_subtasks = []
        self.current_task_name_list = []
        print("dupa pull task list")

        # obtain task name list
        for task in self.current_task_list:
            self.current_task_name_list.append(task.name)
        print("dupa obtain task name list")

        # set new task list
        self.task_list.clear()
        self.task_list.addItems(self.current_task_name_list)

        # clear detail fields
        self.clear_detail_fields()

        # enabling buttons
        if len(self.current_task_list) == 0:
            self.set_buttons_state(False)
        else:
            self.set_buttons_state(True)

    def task_clicked(self):
        """displays the details of the selected task"""
        index = self.task_list.currentRow()
        task = self.current_task_list[index]
        self.current_task = task
        self.current_subtasks = task.subtasks.values()

        if task.is_checked:
            self.task_state_label.setText(self.language_dict["true"])
        else:
            self.task_state_label.setText(self.language_dict["false"])
        self.name_field.setText(task.name)
        self.task_deadline_label.setStyleSheet(code_color_dict[task.priority])
        self.cat_field.setText(task.cat)
        self.desc_field.setText(task.desc) if task.desc is not None else self.desc_field.setText("")
        self.deadline_field.setDate(task.deadline) if task.deadline is not None else self.deadline_field.clear()
        self.none_label.setText("") if task.deadline is not None else self.none_label.setText(self.language_dict["none_label"])
        self.exec_date_field.setDate(task.exec_date) if task.exec_date is not None else self.exec_date_field.clear()
        self.none_label2.setText("") if task.deadline is not None else self.none_label.setText(self.language_dict["none_label"])
        self.subtask_list.clear()
        self.subtask_list.addItems(task.subtasks.values())

    def subtask_clicked(self):
        """sets the state of the subtask checkbox in accordance with the current state of the subtask"""
        current_subtask_index = self.subtask_list.currentRow()
        subtask_state = self.current_task.subtasks[self.current_subtasks[current_subtask_index]]
        if subtask_state:
            self.subtask_state_label.setText(self.language_dict["true"])
        else:
            self.task_state_label.setText(self.language_dict["false"])

    def task_toggled(self):
        self.tasker.toggle_task(self.current_task.task_id)
        if self.current_task.is_checked:
            self.task_state_label.setText(self.language_dict["true"])
        else:
            self.task_state_label.setText(self.language_dict["false"])

    def subtask_toggled(self):
        self.tasker.toggle_subtask(self.current_task.task_id, self.current_subtasks[self.subtask_list.currentRow()])
        if self.current_task.subtasks[self.current_subtasks[self.subtask_list.currentRow()]]:
            self.subtask_state_label.setText(self.language_dict["true"])
        else:
            self.subtask_state_label.setText(self.language_dict["false"])

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

    def settings_window_show(self):
        self.settings_window = SettingsWindow(self, self.tasker, self.settings)
        self.settings_window.show()

    def choose_as_template(self):
        pass

    def choose_date(self):
        chosen_date = datetime(year=self.date_field.date().year(), month=self.date_field.date().month(), day=self.date_field.date().day())
        self.pull_task_list(chosen_date)

    def update_window(self):
        """updates the info after coming back to this window"""
        self.update_settings()
        self.update_text()
        self.set_initial_buttons_state()

    def set_initial_buttons_and_fields_state(self):
        self.current_task_list = []
        self.current_task = None
        self.current_subtasks = []
        self.current_task_name_list = []
        self.clear_detail_fields()
        self.set_buttons_state(False)

    def clear_detail_fields(self):
        self.name_field.setText("")
        self.task_deadline_label.setStyleSheet(code_color_dict[3])
        self.cat_field.setText("")
        self.desc_field.setText("")
        self.deadline_field.clear()
        self.none_label.setText(self.language_dict["none_label"])
        self.none_label2.setText(self.language_dict["none_label"])
        self.exec_date_field.clear()
        self.subtask_list.clear()
        self.task_state_label.setText(self.language_dict["false"])
        self.subtask_state_label.setText(self.language_dict["false"])

    def set_buttons_state(self, state: bool):
        self.template_button.setEnabled(state)
        self.task_checkbox_button.setEnabled(state)
        self.subtask_checkbox_button.setEnabled(state)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_to_main_window()
        a0.ignore()