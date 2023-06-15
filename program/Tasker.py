from sqlalchemy.orm import Session

from program import db_tables
from program.selecter import by_ddl, by_category, by_checked_off_date, by_exec_date
from program.selecter import by_ddl, by_category, by_checked_off_date, by_exec_date, \
    get_category_name, get_category_list, get_category_id, unchecked_tasks
from sqlalchemy import create_engine, update, delete
from datetime import datetime, timedelta
from program.db_tables import Tasks, Subtasks
from program.db_tables import db_name
from program.Task import Task


class Tasker:
    """This class handles adding, loading and editing tasks"""

    def __init__(self, priorities_dict, daily_list_prior_lvl):
        self.current_task_dict = None
        self.get_today_list()
        self.engine = create_engine(db_name, echo=True)
        # TODO na razie niech bedzie verbose zeby ogladac co sie dzieje, potem to zmienimy
        self.priority_dict = priorities_dict
        # A dictionary with default priority level settings:
        # level 0 - urgent
        # level 1 - coming
        # level 2 - far
        self.daily_list_priority_lvl = daily_list_prior_lvl

    def get_current_list(self):
        """Returns the current tasks in a sorted list"""
        curr_task_list = list(self.current_task_dict.values())
        curr_task_list = sorted(curr_task_list)
        return curr_task_list

    def _from_task_tuple_to_task(self, task_tuple):
        task_id, name, cat_id, task_desc, exec_date, deadline, is_checked, checked_off_date = task_tuple
        cat_name = get_category_name(cat_id, self.engine)
        priority = self._calculate_priority(deadline)
        return task_id, Task(task_id=task_id, name=name, cat=cat_name, desc=task_desc, exec_date=exec_date,
                             deadline=deadline, is_checked=is_checked, checked_off_date=checked_off_date,
                             priority=priority)

    def get_by_category(self, cat_name):
        """Fills Tasker's current task dictionary with all unchecked tasks from a given category"""
        cat_id = get_category_id(cat_name, self.engine)[0]
        task_tuple_list = by_category(cat_id, self.engine)
        task_dict = {}
        for task_tuple in task_tuple_list:
            task_id, task = self._from_task_tuple_to_task(task_tuple)
            task_dict[task_id] = task

        self.current_task_dict = task_dict

    def get_today_list(self):
        """Fills Tasker's current task dictionary with all tasks from the daily list"""
        priority_lvl_window = self.priority_dict[self.daily_list_priority_lvl]
        today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        expected_deadline_date = today_date + timedelta(priority_lvl_window)
        task_tuple_list_ddl = by_ddl(expected_deadline_date, self.engine)
        task_tuple_list_exec = by_exec_date(today_date, self.engine)
        task_dict = {}

        for task_tuple in task_tuple_list_ddl:
            task_id, task = self._from_task_tuple_to_task(task_tuple)
            task_dict[task_id] = task
        for task_tuple in task_tuple_list_exec:
            task_id, task = self._from_task_tuple_to_task(task_tuple)
            task_dict[task_id] = task

        self.current_task_dict = task_dict

    def get_by_checked_off_date(self, checked_off_date: datetime):
        """Fills Tasker's current task dictionary with all checked-off tasks with a given check-off date"""
        task_tuple_list = by_checked_off_date(checked_off_date, self.engine)
        task_dict = {}
        for task_tuple in task_tuple_list:
            task_id, task = self._from_task_tuple_to_task(task_tuple)
            task_dict[task_id] = task

        self.current_task_dict = task_dict

    def get_all_unchecked(self):
        """Fills Tasker's current task dictionary with all unchecked tasks"""
        task_tuple_list = unchecked_tasks(self.engine)
        task_dict = {}
        for task_tuple in task_tuple_list:
            task_id, task = self._from_task_tuple_to_task(task_tuple)
            task_dict[task_id] = task

        self.current_task_dict = task_dict

    def category_list(self):
        """Returns a list of all categories"""
        category_tuple_list = get_category_list(self.engine)
        cat_list = []
        for cat_tuple in category_tuple_list:
            cat_id, cat_name = cat_tuple
            cat_list.append(cat_name)
        return cat_list

    def change_priority_lvl_settings(self, urgent: int, coming: int, far: int):
        """Changes priority level settings (time windows assigned to each priority level) in the current app run"""
        self.priority_dict[0] = urgent
        self.priority_dict[1] = coming
        self.priority_dict[2] = far

    def change_daily_list_priority_level_setting(self, new_lvl: int):
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
        """Adds a new task to the database"""
        task_priority = self._calculate_priority(deadline)
        cat_id = get_category_id(cat, self.engine)
        with Session(self.engine) as session:
            task = Tasks(task_id=task_id, name=name, cat=cat_id, desc=desc, exec_date=exec_date,
                         deadline=deadline, is_checked=is_checked, checked_off_date=checked_off_date,
                         task_priority=task_priority)
            session.add(task)
            session.commit()

    def add_subtask(self, task_id, subtask_name):
        with Session(self.engine) as session:
            subtask = Subtasks(parent_task_id=task_id, name=subtask_name, is_checked=False)
            session.add(subtask)
            session.commit()

    def delete_task(self, task_id):
        """Deletes given task locally and in the database"""
        del self.current_task_dict[task_id]
        """query1 = (delete(Subtasks)
                  .where(Subtasks.parent_task_id == task_id))
        """
        query2 = (delete(Tasks)
                  .where(Tasks.task_id == task_id))

        with self.engine.begin() as conn:
            #conn.execute(query1)
            conn.execute(query2)

    def delete_all_checked_off(self):
        "Deletes all tasks in the database that have been checked off"
        query = delete(Subtasks).where(Subtasks.checked_off == True)

        with self.engine.begin() as conn:
            conn.execute(query)

    def delete_subtask(self, task_id, subtask_name):
        """Deletes a given subtask"""
        query = (delete(Subtasks)
                 .where(Subtasks.parent_task_id == task_id)
                 .where(Subtasks.name == subtask_name))

        with self.engine.begin() as conn:
            conn.execute(query)

    def toggle_task(self, task_id):
        """Changes the state of a chosen, stored task and updates database"""
        task = self.current_task_dict[task_id]
        task.toggle() # TODO pointer or copy??
        query = (update(Tasks)
                 .where(Tasks.task_id == task_id)
                 .values(is_checked=task.is_checked, checked_off_date=task.checked_off_date))

        with self.engine.begin() as conn:
            conn.execute(query)

    def toggle_subtask(self, task_id, subtask_name):
        """Changes the state of a chosen, stored subtask and updates database"""
        task = self.current_task_dict[task_id]
        task.toggle_subtask(subtask_name) # TODO as above
        query = (update(Subtasks)
                 .where(Subtasks.parent_task_id == task_id)
                 .where(Subtasks.name == subtask_name)
                 .values(is_checked=task.subtasks[subtask_name][1]))

        with self.engine.begin() as conn:
            conn.execute(query)
