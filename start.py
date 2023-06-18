from gui.main_window import MainWindow
from program.Settings import Settings
from program.Tasker import Tasker
from PyQt5.QtWidgets import QApplication
from datetime import datetime
import sys
from program.selecter import get_category_id, by_category, get_category_name, by_ddl

if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = Settings()
    tasker = Tasker(settings.priority_dict, settings.daily_list_priority_lvl)
    # tasker.add_category("katA")
    # tasker.add_category("katB")
    # tasker.add_task("posprzataj","katA","opis taska posprzataj",datetime(2023,6,18),datetime(2023,6,19),[])
    # tasker.add_task("obiad","katA","opis taska obiad",datetime(2023,6,18),None,[])
    # tasker.add_task("a","katA","opis taska a",datetime(2023,6,18),datetime(2023,6,19),[])
    # tasker.add_task("b","katA","opis taska b",datetime(2023,6,18),datetime(2023,6,19),[])
    # tasker.add_task("c","katA","opis taska c",datetime(2023,6,18),datetime(2023,6,19),[])
    window = MainWindow(tasker, settings)
    window.show()

    sys.exit(app.exec())