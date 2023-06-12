from program.select import by_ddl, by_category, by_checked_off_date, by_exec_date
from sqlalchemy import create_engine
from datetime import datetime

# TODO uzupelnic nazwe databazy - i tak bedzie jedna nasza wiec wystarczy jako zmienna wyszczegolniona w programie
db_name = ...


class Tasker:

    def __init__(self):
        self.current_task_list = self.get_today_list()
        self.engine = create_engine(db_name, echo=True)
        # na razie niech bedzie verbose zeby ogladac co sie dzieje, potem to zmienimy

    def get_by_category(self, cat_id):
        task_tuple_list = by_category(cat_id, self.engine)
        # TODO - find out the format of the output of the selecting function, then proceed
        task_list = []
        return task_list

    def get_today_list(self):
        task_tuple_list = ...
        task_list = []
        return task_list

    def get_by_checked_off_date(self, checked_off_date: datetime):
        task_list = []
        return task_list

    def load_settings(self):
        ...
