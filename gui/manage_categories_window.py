from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QListWidget, QSizePolicy, QSpacerItem,QMessageBox
from PyQt5 import QtGui
from program.language_options import language_options
from program.Settings import Settings
from program.Tasker import Tasker
from gui.add_category_window import AddCategoryWindow


class ManageCategoriesWindow(QWidget):

    def __init__(self, parent, tasker: Tasker, settings: Settings):
        super().__init__()

        self.parent_widget = parent
        self.tasker = tasker
        self.settings = settings
        self.category_list = self.get_categories()
        self.language_setting = None
        self.language_dict = {}

        # hide parent window
        self.parent_widget.hide()

        self.language_settings()

        # main window properties
        self.setWindowTitle(self.language_dict["cat_label"])
        self.setGeometry(100, 100, 680, 400)

        # widgets
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.top_widget.setFixedSize(680, 60)
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
        self.add_category_button.clicked.connect(self.add_category_window_show)
        self.delete_category_button.clicked.connect(self.del_category)

    def language_settings(self):
        self.language_setting = self.settings.language_option
        self.language_dict = language_options[self.language_setting]

    def update_text(self):
        self.setWindowTitle(self.language_dict["cat_label"])
        self.back_button.setText(self.language_dict["back_button"])
        self.add_category_button.setText(self.language_dict["add_category_button"])
        self.delete_category_button.setText(self.language_dict["delete_category_button"])
        self.title_label.setText(self.language_dict["category_window_title"])

    def get_categories(self):
        return self.tasker.category_list()

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

    def update_window(self):
        self.language_settings()
        self.update_text()
        self.category_list = self.get_categories()
        self.cat_list_widget.clear()
        self.cat_list_widget.addItems(self.category_list)

    def add_category_window_show(self):
        self.add_category_window = AddCategoryWindow(self, self.tasker, self.settings)
        self.add_category_window.show()

    def del_category(self):
        cat_name = self.cat_list_widget.currentItem().text()
        successful = self.tasker.delete_category(cat_name)
        if not successful:
            self.msg_box = QMessageBox()
            self.msg_box.setText(self.language_dict["cant_del_cat_msg_box_text"])
            self.msg_box.setWindowTitle(self.language_dict["cant_del_cat_msg_box_title"])
            self.msg_box.setStandardButtons(QMessageBox.Ok)
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.exec()
        else:
            self.category_list = self.get_categories()
            self.cat_list_widget.clear()
            self.cat_list_widget.addItems(self.category_list)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_to_main_window()
        a0.ignore()
