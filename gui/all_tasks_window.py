from typing import List

from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QTabWidget, QListWidget
from PyQt5.QtGui import QIcon, QColorConstants
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtGui
from program.language_options import language_options
from program.Task import Task
import os
from gui.checked_tasks_window import CheckedTasksWindow
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


class AllTasksWindow(QWidget):
    def __init__(self, parent, tasker, settings):
        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings
        self.categories = self.get_category_list()
        self.current_task_list: List[Task] = []
        self.current_task_name_list: List[str] = []
        self.current_task: Task = None
        self.current_subtasks = []
        self.current_category = self.categories[0]
        self.language_setting = None
        self.language_dict = {}

        # hide parent window
        self.parent_widget.hide()

        self.update_settings()

        # main window properties
        self.setWindowTitle(self.language_dict["all_tasks_window_title"])
        self.setGeometry(100, 100, 940, 800)

        # widgets
        self.main_widget = QWidget()
        self.top_actions_widget = QWidget()
        self.top_actions_widget.setFixedSize(940, 75)
        self.tab_widget = QWidget()
        self.tab_widget.setFixedSize(940, 50)
        self.central_content_widget = QWidget()
        self.task_list_widget = QWidget()
        self.detail_widget = QWidget()
        self.task_details_widget = QWidget()
        self.task_actions_widget = QWidget()

        self.left_buttons_widget = QWidget()
        self.left_buttons_widget.setFixedSize(350, 50)
        self.right_buttons_widget = QWidget()
        self.right_buttons_widget.setFixedSize(350, 60)

        self.deadline_widget = QWidget()
        self.exec_date_widget = QWidget()

        # layouts
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_actions_layout = QHBoxLayout()
        self.top_actions_widget.setLayout(self.top_actions_layout)

        self.tab_layout = QVBoxLayout()
        self.tab_widget.setLayout(self.tab_layout)

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

        # checkbox replacement
        self.task_checkbox_button = QPushButton()
        self.task_checkbox_button.setFixedSize(200, 27)
        self.task_checkbox_button.setText(self.language_dict["task_checkbox_button"])
        self.subtask_checkbox_button = QPushButton()
        self.subtask_checkbox_button.setFixedSize(200, 27)
        self.subtask_checkbox_button.setText(self.language_dict["subtask_checkbox_button"])

        # buttons
        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])
        self.checked_tasks_button = QPushButton()
        self.checked_tasks_button.setText(self.language_dict["checked_tasks_button"])
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
        self.new_subtask_button = QPushButton()
        self.new_subtask_button.setText(self.language_dict["new_subtask_button"])
        self.delete_task_button = QPushButton()
        self.delete_task_button.setText(self.language_dict["delete_task_button"])
        self.delete_subtask_button = QPushButton()
        self.delete_subtask_button.setText(self.language_dict["delete_subtask_button"])

        # text_fields
        self.name_field = QLineEdit()
        self.name_field.setEnabled(False)
        self.desc_field = QLineEdit()
        self.desc_field.setEnabled(False)
        self.deadline_field = QDateEdit()
        self.deadline_field.setEnabled(False)
        self.exec_date_field = QDateEdit()
        self.exec_date_field.setEnabled(False)


        # list widgets
        self.task_list = QListWidget()
        self.subtask_list = QListWidget()

        # text labels
        self.task_name_label = QLabel(self.language_dict["task_name_label"])
        self.task_desc_label = QLabel(self.language_dict["task_desc_label"])
        self.task_deadline_label = QLabel(self.language_dict["task_deadline_label"])
        self.task_exec_date_label = QLabel(self.language_dict["task_exec_date_label"])
        self.subtasks_label = QLabel(self.language_dict["subtasks_label"])
        self.none_label = QLabel("")
        self.none_label2 = QLabel("")

        self.task_state_label = QLabel(self.language_dict["false"])
        self.subtask_state_label = QLabel(self.language_dict["false"])

        # tabs (there's so much code in there bc they're 'fake' tabs)
        number_of_tabs = len(self.categories)
        placeholders = []
        for _ in range(number_of_tabs):
            placeholders.append(QLabel())
        self.tabs = QTabWidget()
        for i in range(number_of_tabs):
            self.tabs.addTab(placeholders[i], self.categories[i])
        self.tabs.setFixedSize(940, 27)

        # arrange main window
        self.self_layout = QHBoxLayout()
        self.self_layout.addWidget(self.main_widget)
        self.setLayout(self.self_layout)

        # arrange main widget
        self.main_layout.addWidget(self.top_actions_widget)
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addWidget(self.central_content_widget)

        # arrange top actions widget
        self.top_actions_layout.addWidget(self.left_buttons_widget, alignment=Qt.AlignLeft)
        self.top_actions_layout.addWidget(self.right_buttons_widget, alignment=Qt.AlignRight)

        # arrange left buttons
        self.left_buttons_layout.addWidget(self.back_button)
        self.left_buttons_layout.addWidget(self.checked_tasks_button)

        # arrange right buttons
        self.right_buttons_layout.addWidget(self.action_menu_button)
        self.right_buttons_layout.addWidget(self.settings_button)
        self.right_buttons_layout.addWidget(self.add_task_button)

        # arrange tab widget
        self.tab_layout.addWidget(self.tabs)

        # arrange central content widget
        self.central_content_layout.addWidget(self.task_list_widget)
        self.central_content_layout.addWidget(self.detail_widget)

        # arrange task list widget
        self.task_list_layout.addWidget(self.task_list)

        # arrange detail widget
        self.detail_layout.addWidget(self.task_details_widget)
        self.detail_layout.addWidget(self.task_actions_widget)

        # arrange task det widget
        self.task_details_layout.addWidget(self.task_state_label, alignment=Qt.AlignCenter)
        self.task_details_layout.addWidget(self.task_checkbox_button, alignment=Qt.AlignCenter)
        self.task_details_layout.addWidget(self.task_name_label)
        self.task_details_layout.addWidget(self.name_field)
        self.task_details_layout.addWidget(self.task_desc_label)
        self.task_details_layout.addWidget(self.desc_field)
        self.task_details_layout.addWidget(self.task_deadline_label)
        self.task_details_layout.addWidget(self.deadline_widget)
        self.task_details_layout.addWidget(self.task_exec_date_label)
        self.task_details_layout.addWidget(self.exec_date_widget)
        self.task_details_layout.addWidget(self.subtasks_label)
        self.task_details_layout.addWidget(self.subtask_list)
        self.task_details_layout.addWidget(self.subtask_state_label, alignment=Qt.AlignCenter)
        self.task_details_layout.addWidget(self.subtask_checkbox_button, alignment=Qt.AlignCenter)

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

        # button events
        self.tabs.tabBarClicked.connect(self.changed_category)
        self.back_button.clicked.connect(self.back_to_main_window)
        self.checked_tasks_button.clicked.connect(self.checked_tasks_window_show)
        self.add_task_button.clicked.connect(self.add_task_window_show)
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

    def update_settings(self):
        """updates language settings"""
        self.language_setting = self.settings.language_option
        self.language_dict = language_options[self.language_setting]

    def update_text(self):
        """updates all the text displaying in the window in case the language settings have been changed"""
        self.setWindowTitle(self.language_dict["all_tasks_window_title"])
        self.task_checkbox_button.setText(self.language_dict["task_checkbox_button"])
        self.subtask_checkbox_button.setText(self.language_dict["subtask_checkbox_button"])
        self.back_button.setText(self.language_dict["back_button"])
        self.checked_tasks_button.setText(self.language_dict["checked_tasks_button"])
        self.action_menu_button.setText(self.language_dict["action_menu_button"])
        self.new_subtask_button.setText(self.language_dict["new_subtask_button"])
        self.delete_task_button.setText(self.language_dict["delete_task_button"])
        self.delete_subtask_button.setText(self.language_dict["delete_subtask_button"])
        self.task_name_label.setText(self.language_dict["task_name_label"])
        self.task_desc_label.setText(self.language_dict["task_desc_label"])
        self.task_deadline_label.setText(self.language_dict["task_deadline_label"])
        self.task_exec_date_label.setText(self.language_dict["task_exec_date_label"])
        self.subtasks_label.setText(self.language_dict["subtasks_label"])
        self.none_label.setText(self.language_dict["none_label"])
        self.none_label2.setText(self.language_dict["none_label"])
        self.task_state_label.setText(self.language_dict["false"])
        self.subtask_state_label.setText(self.language_dict["false"])

    def pull_task_list(self):
        # pull task list
        self.tasker.get_by_category(self.current_category)
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
        self.desc_field.setText("")
        self.deadline_field.clear()
        self.none_label.setText(self.language_dict["none_label"])
        self.none_label2.setText(self.language_dict["none_label"])
        self.exec_date_field.clear()
        self.subtask_list.clear()
        self.task_state_label.setText(self.language_dict["false"])
        self.subtask_state_label.setText(self.language_dict["false"])

        # enabling buttons
        self.enable_buttons(False)

    def task_clicked(self):
        """displays the details of the selected task"""
        self.enable_buttons(True)
        self.subtask_checkbox_button.setEnabled(False)

        index = self.task_list.currentRow()
        task = self.current_task_list[index]
        self.current_task = task
        self.current_subtasks = list(task.subtasks.keys())

        if task.is_checked:
            self.task_state_label.setText(self.language_dict["true"])
        else:
            self.task_state_label.setText(self.language_dict["false"])
        self.name_field.setText(task.name)
        self.task_deadline_label.setStyleSheet(code_color_dict[task.priority])
        self.desc_field.setText(task.desc) if task.desc is not None else self.desc_field.setText("")
        self.deadline_field.setDate(task.deadline) if task.deadline is not None else self.deadline_field.clear()
        self.none_label.setText("") if task.deadline is not None else self.none_label.setText(self.language_dict["none_label"])
        self.exec_date_field.setDate(task.exec_date) if task.exec_date is not None else self.exec_date_field.clear()
        self.none_label2.setText("") if task.exec_date is not None else self.none_label.setText(self.language_dict["none_label"])
        self.subtask_list.clear()
        self.subtask_list.addItems(self.current_subtasks)
        self.subtask_state_label.setText(self.language_dict["false"])

        for i in range(len(self.current_subtasks)):
            if self.current_task.subtasks[self.current_subtasks[i]]:
                self.subtask_list.item(i).setBackground(QColorConstants.LightGray)

    def subtask_clicked(self):
        """sets the state of the subtask checkbox in accordance with the current state of the subtask"""
        self.subtask_checkbox_button.setEnabled(True)
        current_subtask_index = self.subtask_list.currentRow()
        subtask_state = self.current_task.subtasks[self.current_subtasks[current_subtask_index]]
        if subtask_state:
            self.subtask_state_label.setText(self.language_dict["true"])
        else:
            self.subtask_state_label.setText(self.language_dict["false"])

    def task_toggled(self):
        """toggles the task in database and in the current list"""
        self.tasker.toggle_task(self.current_task.task_id)
        if self.current_task.is_checked:
            self.task_state_label.setText(self.language_dict["true"])
            self.task_list.currentItem().setBackground(QColorConstants.LightGray)
        else:
            self.task_state_label.setText(self.language_dict["false"])
            self.task_list.currentItem().setBackground(QColorConstants.White)

    def subtask_toggled(self):
        """toggles the subtask in database and in the current list"""
        self.tasker.toggle_subtask(self.current_task.task_id, self.current_subtasks[self.subtask_list.currentRow()])
        if self.current_task.subtasks[self.current_subtasks[self.subtask_list.currentRow()]]:
            self.subtask_state_label.setText(self.language_dict["true"])
            self.subtask_list.currentItem().setBackground(QColorConstants.LightGray)
        else:
            self.subtask_state_label.setText(self.language_dict["false"])
            self.subtask_list.currentItem().setBackground(QColorConstants.White)

    def enable_buttons(self, state):
        self.new_subtask_button.setEnabled(state)
        self.delete_subtask_button.setEnabled(state)
        self.delete_task_button.setEnabled(state)
        self.task_checkbox_button.setEnabled(state)
        self.subtask_checkbox_button.setEnabled(state)

    def changed_category(self, index):
        self.current_category = self.categories[index]
        self.pull_task_list()

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

    def get_category_list(self):
        return self.tasker.category_list()

    def update_window(self):
        """updates the info after coming back to this window"""
        self.update_settings()
        self.update_text()
        self.categories = self.get_category_list()
        self.update_tabs()
        self.pull_task_list()

    def update_tabs(self):
        number_of_tabs = len(self.categories)
        placeholders = []
        for _ in range(number_of_tabs):
            placeholders.append(QLabel())
        self.tabs.clear()
        for i in range(number_of_tabs):
            self.tabs.addTab(placeholders[i], self.categories[i])

    def checked_tasks_window_show(self):
        self.checked_tasks_window = CheckedTasksWindow(self, self.tasker, self.settings)
        self.checked_tasks_window.show()

    def add_task_window_show(self):
        self.add_task_window = AddTaskWindow(self, self.tasker, self.settings, None)
        self.add_task_window.show()

    def add_subtask_window_show(self):
        self.add_subtask_window = AddSubtaskWindow(self, self.tasker, self.settings, self.current_task.task_id)
        self.add_subtask_window.show()

    def action_menu_window_show(self):
        self.action_menu_window = ActionMenuWindow(self, self.tasker, self.settings)
        self.action_menu_window.show()

    def settings_window_show(self):
        self.settings_window = SettingsWindow(self, self.tasker, self.settings)
        self.settings_window.show()

    def delete_subtask(self):
        current_subtask_index = self.subtask_list.currentRow()
        self.tasker.delete_subtask(self.current_task.task_id, self.current_subtasks[current_subtask_index])
        self.pull_task_list()

    def delete_task(self):
        self.tasker.delete_task(self.current_task.task_id)
        self.pull_task_list()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_to_main_window()
        a0.ignore()
