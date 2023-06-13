import functools
from datetime import datetime


@functools.total_ordering
class Task:
    """Class for local (in an app) representation of a task"""

    def __init__(self, task_id: int, name: str, cat: str, desc: str, exec_date: datetime, deadline: datetime,
                 is_checked: bool, checked_off_date: datetime, priority: int):
        self.task_id = task_id
        self.name = name
        self.cat = cat
        self.desc = desc
        self.exec_date = exec_date
        self.deadline = deadline
        self.is_checked = is_checked
        self.checked_off_date = checked_off_date
        self.priority = priority

    def __str__(self):
        return f"Id: {self.task_id}, name: {self.name}, category: {self.cat}, is checked? {self.is_checked}"

    def __eq__(self, other: "Task"):
        return self.deadline == other.deadline

    def __lt__(self, other: "Task"):
        return self.deadline < other.deadline
