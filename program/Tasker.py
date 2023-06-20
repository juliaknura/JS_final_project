from typing import Optional

from sqlalchemy.orm import Session

from program import ania_mode
from program.selecter import by_ddl, by_category, by_checked_off_date, by_exec_date, \
    get_category_name, get_category_list, get_category_id, unchecked_tasks, get_subtasks, checked_off_tasks, \
    by_category_all
from sqlalchemy import create_engine, update, delete
from datetime import datetime, timedelta
from program.db_tables import Tasks, Subtasks, Categories
from program.db_tables import db
from program.Task import Task


class Tasker:
    """This class handles adding, loading and editing tasks"""

    def __init__(self, priorities_dict, daily_list_prior_lvl):
        self.current_task_dict = None
        self.engine = create_engine(db, echo=True)
        # TODO na razie niech bedzie verbose zeby ogladac co sie dzieje, potem to zmienimy
        self.priority_dict = priorities_dict
        # A dictionary with default priority level settings:
        # level 0 - urgent
        # level 1 - coming
        # level 2 - far
        self.daily_list_priority_lvl = daily_list_prior_lvl
        # self.get_today_list()

    def get_current_list(self):
        """Returns the current tasks in a sorted list"""
        curr_task_list = list(self.current_task_dict.values())
        curr_task_list = sorted(curr_task_list)
        return curr_task_list

    def _from_task_tuple_to_task(self, task_entry):
        cat_name = get_category_name(task_entry.cat_id, self.engine)[0]  # switches cat_id with category name

        priority = self._calculate_priority(task_entry.deadline)  # assigns priority

        subtask_list = get_subtasks(task_entry.task_id, self.engine)  # pulls subtask list from database
        subtask_dict = {}
        for subtask in subtask_list:
            name, is_sub_checked = subtask
            subtask_dict[name] = is_sub_checked
        return task_entry.task_id, Task(task_id=task_entry.task_id, name=task_entry.name, cat=cat_name,
                                        desc=task_entry.task_desc, exec_date=task_entry.exec_date,
                                        deadline=task_entry.deadline, is_checked=task_entry.is_checked,
                                        checked_off_date=task_entry.checked_off_date,
                                        priority=priority, subtasks=subtask_dict)

    def get_by_category(self, cat_name):
        """Fills Tasker's current task dictionary with all unchecked tasks from a given category"""
        cat_id = get_category_id(cat_name, self.engine)[0]
        task_db_entries = by_category(cat_id, self.engine)
        task_dict = {}
        for task_entries in task_db_entries:
            task_id, task = self._from_task_tuple_to_task(task_entries[0])
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
            task_id, task = self._from_task_tuple_to_task(task_tuple[0])
            task_dict[task_id] = task
        for task_tuple in task_tuple_list_exec:
            task_id, task = self._from_task_tuple_to_task(task_tuple[0])
            task_dict[task_id] = task

        self.current_task_dict = task_dict

    def get_by_checked_off_date(self, checked_off_date: datetime):
        """Fills Tasker's current task dictionary with all checked-off tasks with a given check-off date"""
        task_tuple_list = by_checked_off_date(checked_off_date, self.engine)
        task_dict = {}
        for task_tuple in task_tuple_list:
            task_id, task = self._from_task_tuple_to_task(task_tuple[0])
            task_dict[task_id] = task

        self.current_task_dict = task_dict

    def get_all_unchecked(self):
        """Fills Tasker's current task dictionary with all unchecked tasks"""
        task_tuple_list = unchecked_tasks(self.engine)
        task_dict = {}
        for task_tuple in task_tuple_list:
            task_id, task = self._from_task_tuple_to_task(task_tuple[0])
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

    def _calculate_priority(self, deadline_date: Optional[datetime]):
        """Calculates the number of days left until the deadline (rounds up) and returns priority category"""
        if deadline_date is None:
            return 3
        else:
            normalized_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            days_diff = (deadline_date - normalized_today).days
            urgent_bar = self.priority_dict[0]
            coming_bar = self.priority_dict[1]
            far_bar = self.priority_dict[2]
            if days_diff <= urgent_bar:
                return 0
            elif days_diff <= coming_bar:
                return 1
            elif days_diff <= far_bar:
                return 2
            else:
                return 3

    @ania_mode.add_task_with_ania_mode
    def add_task(self, name: str, cat: str, desc: str, exec_date: datetime, deadline: datetime, subtasks: list):
        """Adds a new task to the database"""
        cat_id = get_category_id(cat, self.engine)[0]
        with Session(self.engine) as session:
            task = Tasks(name=name, cat_id=cat_id, task_desc=desc, exec_date=exec_date,
                         deadline=deadline, is_checked=False, checked_off_date=None)
            session.add(task)
            session.flush()

            for subtask_name in subtasks:
                subtask = Subtasks(name=subtask_name, parent_task_id=task.task_id, is_checked=False)
                session.add(subtask)

            session.commit()

    def add_subtask(self, task_id, subtask_name):
        """Adds subtask locally and in the database. One task can have only one subtask with the same name.
        Return True if succeeded, False otherwise"""
        if subtask_name not in self.current_task_dict[task_id].subtasks.keys():
            self.current_task_dict[task_id].add_subtask(subtask_name)
            with Session(self.engine) as session:
                subtask = Subtasks(parent_task_id=task_id, name=subtask_name, is_checked=False)
                session.add(subtask)
                session.commit()
                return True
        else:
            return False

    def delete_task(self, task_id):
        """Deletes given task locally and in the database"""
        del self.current_task_dict[task_id]

        with Session(self.engine) as session:
            task = session.get(Tasks, task_id)
            session.delete(task)
            session.commit()

    def delete_all_checked_off(self):
        "Deletes all tasks in the database that have been checked off"
        to_del = checked_off_tasks(self.engine)

        with Session(self.engine) as session:
            for task in to_del:
                session.delete(task[0])
            session.commit()

    def delete_subtask(self, task_id, subtask_name):
        """Deletes a given subtask locally and in the database"""
        self.current_task_dict[task_id].delete_subtask(subtask_name)
        query = (delete(Subtasks)
                 .where(Subtasks.parent_task_id == task_id)
                 .where(Subtasks.name == subtask_name))

        with self.engine.begin() as conn:
            conn.execute(query)

    def toggle_task(self, task_id):
        """Changes the state of a chosen, stored task and updates database"""
        task = self.current_task_dict[task_id]
        task.toggle()  # TODO pointer or copy??
        query = (update(Tasks)
                 .where(Tasks.task_id == task_id)
                 .values(is_checked=task.is_checked, checked_off_date=task.checked_off_date))

        with self.engine.begin() as conn:
            conn.execute(query)

    def toggle_subtask(self, task_id, subtask_name):
        """Changes the state of a chosen, stored subtask and updates database"""
        task = self.current_task_dict[task_id]
        task.toggle_subtask(subtask_name)  # TODO as above
        query = (update(Subtasks)
                 .where(Subtasks.parent_task_id == task_id)
                 .where(Subtasks.name == subtask_name)
                 .values(is_checked=task.subtasks[subtask_name]))

        with self.engine.begin() as conn:
            conn.execute(query)

    def modify_task_desc(self, task_id, new_desc):
        """Change task description"""
        task = self.current_task_dict[task_id]
        task.desc = new_desc
        query = (update(Tasks)
                 .where(Tasks.task_id == task_id)
                 .values(task_desc=new_desc))

        with self.engine.begin() as conn:
            conn.execute(query)

    def add_category(self, cat_name):
        """Add category if it isn't already added. Return True if succeeded, False otherwise"""
        if get_category_id(cat_name, self.engine) is None:
            with Session(self.engine) as session:
                cat = Categories(name=cat_name)
                session.add(cat)
                session.commit()
                return True
        else:
            return False

    def delete_category(self, cat_name):
        """Delete category if there aren't any tasks with it. Return True if succeeded, False otherwise"""
        cat_id = get_category_id(cat_name, self.engine)[0]
        if len(by_category_all(cat_id, self.engine)) == 0:
            query = delete(Categories).where(Categories.name == cat_name)

            with self.engine.begin() as conn:
                conn.execute(query)

            return True
        else:
            return False
