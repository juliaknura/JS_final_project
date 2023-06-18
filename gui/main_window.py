from typing import List

from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QMessageBox, QCheckBox, QListWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QRect, QSize, Qt, QDate
from PyQt5 import QtGui
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options
import sys
from program.Settings import Settings
from program.Tasker import Tasker
from program.Task import Task
import os
from gui.all_tasks_window import AllTasksWindow
from gui.add_task_window import AddTaskWindow
from gui.action_menu_window import ActionMenuWindow
from gui.settings_window import SettingsWindow
from gui.add_subtask_window import AddSubtaskWindow


code_color_dict = {
    0: "background-color: red",
    1: "background-color: yellow",
    2: "background-color: green",
    3: "background-color: white"
}

class MainWindow(QMainWindow):

    def __init__(self, mw_tasker: Tasker, mw_settings: Settings):
        super().__init__()

        self.tasker = mw_tasker
        self.settings = mw_settings
        self.current_task_list: List[Task] = []
        self.current_task_name_list: List[str] = []
        self.current_task: Task = None
        self.current_subtasks = []
        self.language_setting = None
        self.language_dict = {}

        self.update_settings()

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

        self.deadline_widget = QWidget()
        self.exec_date_widget = QWidget()

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

        self.deadline_layout = QHBoxLayout()
        self.exec_date_layout = QHBoxLayout()

        # checkbox replacement
        self.task_checkbox_button = QPushButton()
        self.task_checkbox_button.setText(self.language_dict["task_checkbox_button"])
        self.subtask_checkbox_button = QPushButton()
        self.subtask_checkbox_button.setText(self.language_dict["subtask_checkbox_button"])

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
        # self.none_label = QLabel(self.language_dict["none_label"])
        # self.none_label2 = QLabel(self.language_dict["none_label"])
        self.none_label = QLabel("")
        self.none_label2 = QLabel("")
        self.task_state_label = QLabel(self.language_dict["false"])
        self.subtask_state_label = QLabel(self.language_dict["false"])

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
        self.settings_button.setIconSize(QSize(70, 70))
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

        # list widgets
        self.task_list = QListWidget()
        self.subtask_list = QListWidget()

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
        self.task_details_widget.setLayout(self.task_details_layout)

        # arrange deadline widget
        self.deadline_layout.addWidget(self.deadline_field)
        self.deadline_layout.addWidget(self.none_label)
        self.deadline_widget.setLayout(self.deadline_layout)

        # arrange exec date widget
        self.exec_date_layout.addWidget(self.exec_date_field)
        self.exec_date_layout.addWidget(self.none_label2)
        self.exec_date_widget.setLayout(self.exec_date_layout)

        # arrange task actions widget
        self.task_actions_layout.addWidget(self.new_subtask_button)
        self.task_actions_layout.addWidget(self.delete_subtask_button)
        self.task_actions_layout.addWidget(self.delete_task_button)
        self.task_actions_widget.setLayout(self.task_actions_layout)

        # add button functionalities
        self.all_tasks_button.clicked.connect(self.all_tasks_window_show)
        self.new_task_button.clicked.connect(self.add_task_window_show)
        self.action_menu_button.clicked.connect(self.action_menu_window_show)
        self.settings_button.clicked.connect(self.settings_window_show)
        self.new_subtask_button.clicked.connect(self.add_subtask_window_show)
        self.delete_subtask_button.clicked.connect(self.delete_subtask)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.task_checkbox_button.clicked.connect(self.task_toggled)
        self.subtask_checkbox_button.clicked.connect(self.subtask_toggled)
        self.task_list.itemClicked.connect(self.task_clicked)
        self.subtask_list.itemClicked.connect(self.subtask_clicked)

        self.pull_task_list()

    def all_tasks_window_show(self):
        self.all_tasks_window = AllTasksWindow(self, self.tasker, self.settings)
        self.all_tasks_window.show()

    def add_task_window_show(self):
        self.add_task_window = AddTaskWindow(self, self.tasker, self.settings, None)
        self.add_task_window.show()

    def add_subtask_window_show(self):
        self.add_subtask_window = AddSubtaskWindow(self, self.tasker, self.settings)
        self.add_subtask_window.show()

    def action_menu_window_show(self):
        self.action_menu_window = ActionMenuWindow(self, self.tasker, self.settings)
        self.action_menu_window.show()

    def settings_window_show(self):
        self.settings_window = SettingsWindow(self, self.tasker, self.settings)
        self.settings_window.show()

    def delete_subtask(self):
        pass

    def delete_task(self):
        pass

    def update_settings(self):
        """updates language settings"""
        self.language_setting = self.settings.language_option
        self.language_dict = language_options[self.language_setting]

    def update_text(self):
        """updates all the text displaying in the window in case the language settings have been changed"""
        self.setWindowTitle(self.language_dict["main_window_title"])

        self.task_name_label.setText(self.language_dict["task_name_label"])
        self.task_cat_label.setText(self.language_dict["task_cat_label"])
        self.task_desc_label.setText(self.language_dict["task_desc_label"])
        self.task_deadline_label.setText(self.language_dict["task_deadline_label"])
        self.task_exec_date_label.setText(self.language_dict["task_exec_date_label"])
        self.subtasks_label.setText(self.language_dict["subtasks_label"])
        self.daily_title_label.setText(self.language_dict["daily_title_label"])

        self.action_menu_button.setText(self.language_dict["action_menu_button"])
        self.all_tasks_button.setText(self.language_dict["all_tasks_button"])
        self.new_subtask_button.setText(self.language_dict["new_subtask_button"])
        self.delete_task_button.setText(self.language_dict["delete_task_button"])
        self.delete_subtask_button.setText(self.language_dict["delete_subtask_button"])

        self.task_checkbox_button.setText(self.language_dict["task_checkbox_button"])
        self.subtask_checkbox_button.setText(self.language_dict["subtask_checkbox_button"])
        self.task_state_label.setText(self.language_dict["false"])
        self.subtask_state_label.setText(self.language_dict["false"])


    def update_window(self):
        """updates the info after coming back to this window"""
        self.update_settings()
        self.update_text()
        self.pull_task_list()

    def pull_task_list(self):
        # pull task list
        self.tasker.get_today_list()
        self.current_task_list = self.tasker.get_current_list()
        self.current_task = None
        self.current_subtasks = []
        self.current_task_name_list = []

        # obtain task name list
        for task in self.current_task_list:
            self.current_task_name_list.append(task.name)

        # set new task list
        self.task_list.clear()
        self.task_list.addItems(self.current_task_name_list)

        # clear detail fields
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

        # enabling buttons
        if len(self.current_task_list) == 0:
            self.new_subtask_button.setEnabled(False)
            self.delete_subtask_button.setEnabled(False)
            self.delete_task_button.setEnabled(False)
            self.task_checkbox_button.setEnabled(False)
            self.subtask_checkbox_button.setEnabled(False)
        else:
            self.new_subtask_button.setEnabled(True)
            self.delete_subtask_button.setEnabled(True)
            self.delete_task_button.setEnabled(True)
            self.task_checkbox_button.setEnabled(True)
            self.subtask_checkbox_button.setEnabled(True)

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

    def closeEvent(self, a0: QtGui.QCloseEvent):
        reply = QMessageBox.question(self, self.language_dict["quit_confirmation"], self.language_dict["are_you_sure_you_want_to_quit"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            a0.accept()
        else:
            a0.ignore()



