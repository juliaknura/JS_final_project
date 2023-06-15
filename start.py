from gui.main_window import MainWindow
from program.Settings import Settings
from program.Tasker import Tasker
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = Settings()
    tasker = Tasker(settings.priority_dict, settings.daily_list_priority_lvl)
    window = MainWindow(tasker, settings)
    window.show()

    sys.exit(app.exec())
