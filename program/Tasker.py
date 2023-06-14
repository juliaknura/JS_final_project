from sqlalchemy.orm import Session

from program import db_tables
from program.selecter import by_ddl, by_category, by_checked_off_date, by_exec_date
from program.selecter import by_ddl, by_category, by_checked_off_date, by_exec_date, \
    get_category_name, get_category_list, get_category_id, unchecked_tasks
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import json
from program.db_tables import db_name
from program.Task import Task


class Tasker:
    """This class handles adding, loading and editing tasks"""

    def __init__(self): # TODO powinien dostać priority_dict i daily_list_priority_lvl
        self.current_task_list = self.get_today_list()
        self.engine = create_engine(db_name, echo=True)
        # TODO na razie niech bedzie verbose zeby ogladac co sie dzieje, potem to zmienimy
        p_dict, l_opt, d_list_p_lvl = self.load_settings()
        self.priority_dict = p_dict
        # A dictionary with default priority level settings:
        # level 0 - urgent
        # level 1 - coming
        # level 2 - far
        self.language_option = l_opt
        self.daily_list_priority_lvl = d_list_p_lvl

    def _from_task_tuple_to_task(self, task_tuple):
        task_id, name, cat_id, task_desc, exec_date, deadline, is_checked, checked_off_date = task_tuple
        cat_name = get_category_name(cat_id, self.engine)
        priority = self._calculate_priority(deadline)
        return Task(task_id=task_id, name=name, cat=cat_name, desc=task_desc, exec_date=exec_date,
                    deadline=deadline, is_checked=is_checked, checked_off_date=checked_off_date,
                    priority=priority)

    def get_by_category(self, cat_name):
        cat_id = get_category_id(cat_name, self.engine)[0]
        task_tuple_list = by_category(cat_id, self.engine)
        task_list = []
        for task_tuple in task_tuple_list:
            task_list.append(self._from_task_tuple_to_task(task_tuple))

        task_list = sorted(task_list)
        return task_list

    def get_today_list(self):
        priority_lvl_window = self.priority_dict[self.daily_list_priority_lvl]
        today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        expected_deadline_date = today_date + timedelta(priority_lvl_window)
        task_tuple_list_ddl = by_ddl(expected_deadline_date, self.engine)
        task_tuple_list_exec = by_exec_date(today_date, self.engine)
        task_list = []

        for task_tuple in task_tuple_list_ddl:
            task_list.append(self._from_task_tuple_to_task(task_tuple))
        for task_tuple in task_tuple_list_exec:
            task_list.append(self._from_task_tuple_to_task(task_tuple))

        task_list = sorted(task_list)
        return task_list

    def get_by_checked_off_date(self, checked_off_date: datetime):
        task_tuple_list = by_checked_off_date(checked_off_date, self.engine)
        task_list = []
        for task_tuple in task_tuple_list:
            task_list.append(self._from_task_tuple_to_task(task_tuple))
        task_list = sorted(task_list)
        return task_list

    def get_all_unchecked(self):
        task_tuple_list = unchecked_tasks(self.engine)
        task_list = []
        for task_tuple in task_tuple_list:
            task_list.append(self._from_task_tuple_to_task(task_tuple))
        task_list = sorted(task_list)
        return task_list

    def category_list(self):
        category_tuple_list = get_category_list(self.engine)
        cat_list = []
        for cat_tuple in category_tuple_list:
            cat_id, cat_name = cat_tuple
            cat_list.append(cat_name)
        return cat_list

    def change_priority_lvl_settings(self, urgent: int, coming: int, far: int): #TODO ogarnąć
        """Changes priority level settings (time windows assigned to each priority level) in the current app run"""
        self.priority_dict[0] = urgent
        self.priority_dict[1] = coming
        self.priority_dict[2] = far

    def change_daily_list_priority_level_setting(self, new_lvl: int): #TODO ogarnąć
        """Changes daily list priority level setting in the current app run"""
        self.daily_list_priority_lvl = new_lvl

    def _calculate_priority(self, deadline_date: datetime):
        """Calculates the number of days left until the deadline (rounds up) and returns priority category"""
        normalized_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (deadline_date - normalized_today).days
        urgent_bar = self.priority_dict[1]
        coming_bar = self.priority_dict[2]
        far_bar = self.priority_dict[3]
        if days_diff <= urgent_bar:
            return 0
        elif days_diff <= coming_bar:
            return 1
        elif days_diff <= far_bar:
            return 2

    def add_task(self, task_id: int, name: str, cat: str, desc: str, exec_date: datetime, deadline: datetime,
                 is_checked: bool, checked_off_date: datetime):
        """Add a new task to the database"""
        task_priority = self._calculate_priority(deadline)

        with Session(self.engine) as session:
            task = db_tables.Task(task_id, name, cat, desc, exec_date, deadline, is_checked,
                                  checked_off_date, task_priority)
            session.add(task)
            session.commit()