from datetime import datetime

from program.Task import Task


class TaskDecor(Task):
    def __init__(self, task):
        super().__init__(task.task_id, task.name, task.cat, task.desc, task.exec_date, task.deadline, task.is_checked,
                         task.checked_off_date, task.priority)

        self.wrappee = task

    def __str__(self):
        return self.task.__str__()

    def __eq__(self, other: "Task"):
        return self.task.__eq__(other)

    def __lt__(self, other: "Task"):
        return self.task.__lt__(other)

    def toggle(self):
        self.task.toggle()
        self.is_checked = self.task.is_checked
        self.checked_off_date = self.task.checked_off_date
