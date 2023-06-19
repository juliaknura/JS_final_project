from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QSizePolicy, QSpacerItem, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtGui
from program.language_options import language_options
import os
from gui.cat_window import CatWindow
from gui.add_task_window import AddTaskWindow
from gui.manage_categories_window import ManageCategoriesWindow


class ActionMenuWindow(QWidget):

    def __init__(self, parent, tasker, settings):
        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings
        self.language_setting = None
        self.language_dict = {}

        # hide parent window
        self.parent_widget.hide()

        self.language_settings()

        # main window properties
        self.setWindowTitle(self.language_dict["action_menu_window_title"])
        self.setGeometry(100, 100, 430, 400)

        # widgets
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.content_widget = QWidget()
        self.add_widget = QWidget()
        self.del_widget = QWidget()
        self.cat_widget = QWidget()
        self.real_cat_widget = QWidget()

        # layouts

        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        self.add_layout = QHBoxLayout()
        self.add_widget.setLayout(self.add_layout)

        self.del_layout = QHBoxLayout()
        self.del_widget.setLayout(self.del_layout)

        self.cat_layout = QHBoxLayout()
        self.cat_widget.setLayout(self.cat_layout)

        self.real_cat_layout = QHBoxLayout()
        self.real_cat_widget.setLayout(self.real_cat_layout)

        # buttons

        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])

        self.add_task_button = QPushButton()
        self.add_task_button.setIcon(QIcon(os.getcwd() + os.sep + "gui" + os.sep + "plus_icon.png"))
        self.add_task_button.setIconSize(QSize(50, 50))
        self.add_task_button.setFixedSize(60, 60)
        self.add_task_button.show()

        self.del_all_tasks_button = QPushButton()
        self.del_all_tasks_button.setIcon(QIcon(os.getcwd() + os.sep + "gui" + os.sep + "trash_icon.png"))
        self.del_all_tasks_button.setIconSize(QSize(50, 50))
        self.del_all_tasks_button.setFixedSize(60, 60)
        self.del_all_tasks_button.show()

        self.cats_button = QPushButton()
        self.cats_button.setIcon(QIcon(os.getcwd() + os.sep + "gui" + os.sep + "tabs_icon.png"))
        self.cats_button.setIconSize(QSize(50, 50))
        self.cats_button.setFixedSize(60, 60)
        self.cats_button.show()

        self.the_real_cats_button = QPushButton()
        self.the_real_cats_button.setIcon(QIcon(os.getcwd() + os.sep + "gui" + os.sep + "cat_icon.png"))
        self.the_real_cats_button.setIconSize(QSize(50, 50))
        self.the_real_cats_button.setFixedSize(60, 60)
        self.the_real_cats_button.show()

        # labels
        self.title_label = QLabel(self.language_dict["action_menu_title"])
        font = self.title_label.font()
        font.setBold(True)
        font.setPointSize(20)
        self.title_label.setFont(font)
        self.del_all_tasks_label = QLabel(self.language_dict["del_all_tasks_label"])
        self.add_task_label = QLabel(self.language_dict["add_tasks_window_title"])
        self.cat_label = QLabel(self.language_dict["cat_label"])
        self.real_cat_label = QLabel(self.language_dict["real_cat_label"])

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
        self.content_layout.addWidget(self.add_widget)
        self.content_layout.addWidget(self.del_widget)
        self.content_layout.addWidget(self.cat_widget)
        self.content_layout.addWidget(self.real_cat_widget)

        # arrange add widget
        self.add_layout.addWidget(self.add_task_button)
        self.add_layout.addWidget(self.add_task_label)

        # arrange del widget
        self.del_layout.addWidget(self.del_all_tasks_button)
        self.del_layout.addWidget(self.del_all_tasks_label)

        # arrange cat widget
        self.cat_layout.addWidget(self.cats_button)
        self.cat_layout.addWidget(self.cat_label)

        # arrange real cat widget
        self.real_cat_layout.addWidget(self.the_real_cats_button)
        self.real_cat_layout.addWidget(self.real_cat_label)

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)
        self.the_real_cats_button.clicked.connect(self.cat_window_show)
        self.add_task_button.clicked.connect(self.add_task_window_show)
        self.cats_button.clicked.connect(self.manage_categories_window_show)
        self.del_all_tasks_button.clicked.connect(self.delete_all_tasks)

    def language_settings(self):
        self.language_setting = self.settings.language_option
        self.language_dict = language_options[self.language_setting]

    def update_text(self):
        self.setWindowTitle(self.language_dict["action_menu_window_title"])
        self.back_button.setText(self.language_dict["back_button"])
        self.title_label.setText(self.language_dict["action_menu_title"])
        self.del_all_tasks_label.setText(self.language_dict["del_all_tasks_label"])
        self.add_task_label.setText(self.language_dict["add_tasks_window_title"])
        self.cat_label.setText(self.language_dict["cat_label"])
        self.real_cat_label.setText(self.language_dict["real_cat_label"])

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

    def update_window(self):
        self.language_settings()
        self.update_text()

    def cat_window_show(self):
        self.cat_window = CatWindow(self, self.tasker, self.settings)
        self.cat_window.show()

    def add_task_window_show(self):
        self.add_task_window = AddTaskWindow(self, self.tasker, self.settings, None)
        self.add_task_window.show()

    def manage_categories_window_show(self):
        self.manage_categories_window = ManageCategoriesWindow(self, self.tasker, self.settings)
        self.manage_categories_window.show()

    def delete_all_tasks(self):
        self.tasker.delete_all_checked_off()
        self.msg_box = QMessageBox()
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setText(self.language_dict["all_tasks_deleted_msg"])
        self.msg_box.setWindowTitle(self.language_dict["all_tasks_deleted_title"])
        self.msg_box.setStandardButtons(QMessageBox.Ok)
        self.msg_box.exec()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_to_main_window()
        a0.ignore()
