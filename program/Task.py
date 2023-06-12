import functools
from datetime import datetime
from program.settings import priority_dict


@functools.total_ordering
class Task:
    """Class for local (in an app) representation of a task"""

    def __init__(self, task_id: int, name: str, cat: str, desc: str, exec_date: datetime, deadline: datetime,
                 is_checked: bool, checked_off_date: datetime):
        self.task_id = task_id
        self.name = name
        self.cat = cat
        self.desc = desc
        self.exec_date = exec_date
        self.deadline = deadline
        self.is_checked = is_checked
        self.checked_off_date = checked_off_date
        self.priority = self._calculate_priority()
        print(self.priority)

    def __str__(self):
        return f"Id: {self.task_id}, name: {self.name}, category: {self.cat}, is checked? {self.is_checked}"

    def __eq__(self, other: "Task"):
        return self.deadline == other.deadline

    def __lt__(self, other: "Task"):
        return self.deadline < other.deadline

    def _calculate_priority(self):
        """Calculates the number of days left until the deadline (rounds up) and assigns priority category"""
        normalized_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (self.deadline - normalized_today).days
        urgent_bar = priority_dict[1]
        coming_bar = priority_dict[2]
        far_bar = priority_dict[3]
        if days_diff <= urgent_bar:
            return 1
        elif days_diff <= coming_bar:
            return 2
        elif days_diff <= far_bar:
            return 3
