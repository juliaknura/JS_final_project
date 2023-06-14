from program.TaskDecor import TaskDecor


class TaskWithSubtasks(TaskDecor):
    "Tasks with subtasks"
    def __init__(self, task):
        super().__init__(task)
        self.subtasks = dict()

    def add_subtask(self, title, is_done=False):
        self.subtasks[title] = is_done

    def toggle_subtask(self, title):
        if self.subtasks[title]:
            self.subtasks[title] = False
        else:
            self.subtasks[title] = True

    def delete_subtask(self, title):
        del self.subtasks[title]