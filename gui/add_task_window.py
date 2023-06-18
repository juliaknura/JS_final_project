from typing import Optional

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QComboBox, QRadioButton, QListWidget, QSizePolicy, QSpacerItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect, QSize, Qt, QDate
from PyQt5 import QtGui
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options
import sys
from program.Settings import Settings
from program.Tasker import Tasker
from program.Task import Task
import os
from gui.add_subtask_window import AddSubtaskWindow2
from datetime import datetime
from program.ania_mode import create_shopping_task


class AddTaskWindow(QWidget):

    def __init__(self, parent, tasker: Tasker, settings: Settings, template_task: Optional[Task]):

        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings
        self.language_setting = None
        self.language_dict = {}
        self.template_task = template_task
        self.categories_list = self.get_category_list()
        self.added_subtasks_dict = {}

        # hide parent window
        self.parent_widget.hide()

        self.language_settings()

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

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)
        self.new_subtask_button.clicked.connect(self.add_subtask_window_show)
        self.add_button.clicked.connect(self.add_button_event)
        self.delete_subtask_button.clicked.connect(self.delete_subtask)

        self.fill_from_template()

    def language_settings(self):
        self.language_setting = self.settings.language_option
        self.language_dict = language_options[self.language_setting]

    def get_category_list(self):
        return self.tasker.category_list()

    def find_cat_index(self, cat_name):
        i=0
        for elem in self.categories_list:
            if elem == cat_name:
                return i
            else:
                i += 1

    def fill_from_template(self):
        if self.template_task is not None:
            name = self.template_task.name
            cat = self.template_task.cat
            desc= self.template_task.desc
            exec_date = self.template_task.exec_date
            deadline = self.template_task.deadline
            subtasks = self.template_task.subtasks

            self.name_field.setText(name)
            index = self.find_cat_index(cat)
            self.category_combo_box.setCurrentIndex(index)
            if desc is not None:
                self.desc_field.setText(desc)
            if deadline is not None:
                ddl = QDate(deadline.year, deadline.month, deadline.day)
                self.deadline_field.setDate(ddl)
                self.none_deadline.setChecked(False)
            else:
                self.deadline_field.setDate(QDate.currentDate())
                self.none_deadline.setChecked(True)
            if exec_date is not None:
                exec = QDate(exec_date.year,exec_date.month,exec_date.day)
                self.exec_date_field.setDate(exec)
                self.none_exec_date.setChecked(False)
            else:
                self.exec_date_field.setDate(QDate.currentDate())
                self.none_exec_date.setChecked(True)
            self.added_subtasks_dict = subtasks
            self.subtask_list.clear()
            self.subtask_list.addItems(list(self.added_subtasks_dict.keys()))


    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

    def update_window(self):
        pass

    def add_subtask(self, subtask_name):
        self.added_subtasks_dict[subtask_name] = ""
        self.subtask_list.clear()
        self.subtask_list.addItems(list(self.added_subtasks_dict.keys()))

    def add_subtask_window_show(self):
        self.add_subtask_window = AddSubtaskWindow2(self, self.tasker, self.settings)
        self.add_subtask_window.show()

    def add_button_event(self):
        name = self.name_field.text()
        if name == "":
            self.msg_box = QMessageBox()
            self.msg_box.setText(self.language_dict["zero_length_name_msg"])
            self.msg_box.setWindowTitle(self.language_dict["zero_length_name_title"])
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.exec()
        else:
            cat = self.category_combo_box.currentText()
            desc = self.desc_field.text()
            if desc == "":
                desc = None
            if self.none_exec_date.isChecked():
                exec_date = None
            else:
                exec_date = datetime(year=self.exec_date_field.date().year(), month=self.exec_date_field.date().month(),
                                     day=self.exec_date_field.date().day())
            if self.none_deadline.isChecked():
                deadline = None
            else:
                deadline = datetime(year=self.deadline_field.date().year(), month=self.deadline_field.date().month(),
                                    day=self.deadline_field.date().day())
            subtasks = list(self.added_subtasks_dict.keys())

            prompt = self.tasker.add_task(name=name, cat=cat, desc=desc, exec_date=exec_date, deadline=deadline,
                                          subtasks=subtasks)

            if prompt is not None:
                self.msg_box = QMessageBox()
                self.msg_box.setText(self.language_dict["msg_box_text"])
                self.msg_box.setWindowTitle(self.language_dict["msg_box_title"])
                self.msg_box.setIconPixmap(QPixmap(os.getcwd() + os.sep + "gui" + os.sep + "question_mark.png"))
                self.msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                res = self.msg_box.exec()
                if res == QMessageBox.Yes:
                    print("creating shopping task")
                    # create_shopping_task(self.tasker,self.name_field.text(),)
            self.back_to_main_window()

    def delete_subtask(self):
        subtask = self.subtask_list.currentItem().text()
        self.added_subtasks_dict.pop(subtask)
        self.subtask_list.clear()
        self.subtask_list.addItems(list(self.added_subtasks_dict.keys()))

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_to_main_window()
        a0.ignore()
