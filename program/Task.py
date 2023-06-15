import functools
from datetime import datetime
from typing import Optional


@functools.total_ordering
class Task:
    """Class for local (in an app) representation of a task"""

    def __init__(self, task_id: int, name: str, cat: str, desc: Optional[str], exec_date: Optional[datetime],
                 deadline: Optional[datetime], is_checked: bool, checked_off_date: Optional[datetime],
                 priority: int, subtasks: Optional[dict]):
        self.task_id = task_id
        self.name = name
        self.cat = cat
        self.desc = desc
        self.exec_date = exec_date
        self.deadline = deadline
        self.is_checked = is_checked
        self.checked_off_date = checked_off_date
        self.priority = priority
        self.subtasks = subtasks

    def __str__(self):
        return f"Id: {self.task_id}, name: {self.name}, category: {self.cat}, is checked? {self.is_checked}"

    def __eq__(self, other: "Task"):
        if self.deadline is None and other.deadline is None:
            return True
        elif self.deadline is None:
            return False
        elif other.deadline is None:
            return False
        else:
            return self.deadline == other.deadline

    def __lt__(self, other: "Task"):
        if self.deadline is None and other.deadline is None:
            return True
        elif self.deadline is None:
            return False
        elif other.deadline is None:
            return True
        else:
            return self.deadline < other.deadline

    def toggle(self):
        """Switch the state of the task"""
        if self.is_checked:
            self.is_checked = False
            self.checked_off_date = None
        else:
            self.is_checked = True
            self.checked_off_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def add_subtask(self, title, is_done=False):
        """Add a subtask to the task"""
        self.subtasks[title] = is_done

    def toggle_subtask(self, title):
        """Switch the state of a subtask"""
        if self.subtasks[title]:
            self.subtasks[title] = False
        else:
            self.subtasks[title] = True

    def delete_subtask(self, title):
        """Delete a subtask"""
        del self.subtasks[title]
