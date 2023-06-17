from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QPushButton, QLineEdit, QDateEdit, QComboBox, QRadioButton, QListWidget, QSizePolicy, QSpacerItem, QSpinBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5 import QtGui
from pyqt_checkbox_list_widget.checkBoxListWidget import CheckBoxListWidget
from program.language_options import language_options


class SettingsWindow(QWidget):

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

        self.language_options = [self.language_dict["english"], self.language_dict["polish"],
                                 self.language_dict["silly"]]
        self.priority_levels = [self.language_dict["high"], self.language_dict["medium"], self.language_dict["low"]]

        # main window properties
        self.setWindowTitle(self.language_dict["settings_window_title"])
        self.setGeometry(100, 100, 500, 400)


        # widget
        self.main_widget = QWidget()
        self.top_widget = QWidget()
        self.content_widget = QWidget()
        self.language_widget = QWidget()
        self.pr_levels_widget = QWidget()
        self.daily_pr_lev_widget = QWidget()
        self.high_pr_widget = QWidget()
        self.high_pr_widget.setFixedSize(250, 50)
        self.med_pr_widget = QWidget()
        self.med_pr_widget.setFixedSize(250, 50)
        self.low_pr_widget = QWidget()
        self.low_pr_widget.setFixedSize(250, 50)

        # layouts
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.top_widget.setLayout(self.top_layout)

        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        self.language_layout = QHBoxLayout()
        self.language_widget.setLayout(self.language_layout)

        self.pr_levels_layout = QVBoxLayout()
        self.pr_levels_widget.setLayout(self.pr_levels_layout)

        self.daily_pr_lev_layout = QHBoxLayout()
        self.daily_pr_lev_widget.setLayout(self.daily_pr_lev_layout)

        self.high_pr_layout = QHBoxLayout()
        self.high_pr_widget.setLayout(self.high_pr_layout)

        self.med_pr_layout = QHBoxLayout()
        self.med_pr_widget.setLayout(self.med_pr_layout)

        self.low_pr_layout = QHBoxLayout()
        self.low_pr_widget.setLayout(self.low_pr_layout)

        # labels
        self.title_label = QLabel(self.language_dict["settings_title"])
        font = self.title_label.font()
        font.setBold(True)
        font.setPointSize(20)
        self.title_label.setFont(font)
        self.choose_language_option_label = QLabel(self.language_dict["choose_language_option_label"])
        self.choose_pr_lvl_time_windows_label = QLabel(self.language_dict["choose_pr_lvl_time_windows_label"])
        self.high_lvl_label = QLabel(self.language_dict["high_lvl_label"])
        self.med_lvl_label = QLabel(self.language_dict["med_lvl_label"])
        self.low_lvl_label = QLabel(self.language_dict["low_lvl_label"])
        self.choose_pr_lvl_daily_label = QLabel(self.language_dict["choose_pr_lvl_daily_label"])

        # buttons
        self.back_button = QPushButton()
        self.back_button.setText(self.language_dict["back_button"])
        self.save_button = QPushButton()
        self.save_button.setText(self.language_dict["save_button"])
        self.save_button.setFixedSize(50, 27)

        # combo boxes
        self.language_combo_box = QComboBox()
        self.language_combo_box.addItems(self.language_options)

        self.priority_combo_box = QComboBox()
        self.priority_combo_box.addItems(self.priority_levels)

        # spin boxes
        self.high_spin_box = QSpinBox()
        self.high_spin_box.setMinimum(1)
        self.med_spin_box = QSpinBox()
        self.med_spin_box.setMinimum(1)
        self.low_spin_box = QSpinBox()
        self.low_spin_box.setMinimum(1)

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
        self.content_layout.addWidget(self.language_widget)
        self.content_layout.addWidget(self.pr_levels_widget)
        self.content_layout.addWidget(self.daily_pr_lev_widget)
        self.content_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        # arrange priority levels widget
        self.pr_levels_layout.addWidget(self.choose_pr_lvl_time_windows_label)
        self.pr_levels_layout.addWidget(self.high_pr_widget, alignment=Qt.AlignCenter)
        self.pr_levels_layout.addWidget(self.med_pr_widget, alignment=Qt.AlignCenter)
        self.pr_levels_layout.addWidget(self.low_pr_widget, alignment=Qt.AlignCenter)

        # arrange language options widget
        self.language_layout.addWidget(self.choose_language_option_label)
        self.language_layout.addWidget(self.language_combo_box)

        # arrange daily priority widget
        self.daily_pr_lev_layout.addWidget(self.choose_pr_lvl_daily_label)
        self.daily_pr_lev_layout.addWidget(self.priority_combo_box)

        # arrange high widget
        self.high_pr_layout.addWidget(self.high_lvl_label)
        self.high_pr_layout.addWidget(self.high_spin_box)

        # arrange medium widget
        self.med_pr_layout.addWidget(self.med_lvl_label)
        self.med_pr_layout.addWidget(self.med_spin_box)

        # arrange low widget
        self.low_pr_layout.addWidget(self.low_lvl_label)
        self.low_pr_layout.addWidget(self.low_spin_box)

        # button events
        self.back_button.clicked.connect(self.back_to_main_window)

    def back_to_main_window(self):
        self.parent_widget.update_window()
        self.parent_widget.show()
        self.hide()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_to_main_window()
        a0.ignore()
