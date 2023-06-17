from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QComboBox, QRadioButton, QListWidget, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect, QSize, Qt
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options


class AddSubtaskWindow(QWidget):

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
        self.setWindowTitle(self.language_dict["new_subtask_button"])
        self.setGeometry(100, 100, 450, 200)

        # widgets
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.content_widget = QWidget()

        # layouts
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        # labels
        self.title_label = QLabel(self.language_dict["add_subtask_title"])
        font = self.title_label.font()
        font.setBold(True)
        font.setPointSize(20)
        self.title_label.setFont(font)
        self.insert_new_subtask_name_label = QLabel(self.language_dict["insert_new_subtask_name_label"])

        # buttons
        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])

        self.add_subtask_button = QPushButton()
        self.add_subtask_button.setText(self.language_dict["new_subtask_button"])
        self.add_subtask_button.setFixedSize(120, 27)

        # fields
        self.subtask_name_field = QLineEdit()

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
        self.content_layout.addWidget(self.insert_new_subtask_name_label)
        self.content_layout.addWidget(self.subtask_name_field)
        self.content_layout.addWidget(self.add_subtask_button, alignment=Qt.AlignCenter)

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)
        self.add_subtask_button.clicked.connect(self.add_subtask)

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

    def add_subtask(self):
        print("type 1 window")


class AddSubtaskWindow2(AddSubtaskWindow):
    def __init__(self, parent, tasker, settings):
        super().__init__(parent, tasker, settings)

    def add_subtask(self):
        print("type 2 window")
