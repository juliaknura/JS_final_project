import datetime
import os
import pytest as pytest
from program.Task import Task
from program.Tasker import Tasker

os.chdir("../program")


def test_add_delete_category():
    # GIVEN
    priorities = {0: 1, 1: 3, 2: 7}
    suid = Tasker(priorities, 0)
    name = "tajna_kategoria"

    # WHEN
    suid.add_category(name)
    categories = suid.category_list()
    suid.delete_category(name)
    empty_categories = suid.category_list()

    # THEN
    assert categories[0] == name
    assert len(empty_categories) == 0


@pytest.mark.parametrize("name, cat, desc, exec_date, ddl, subtasks", [
    ("odkurzyć", "domowe", "opis opis", datetime.datetime(2023, 7, 13), datetime.datetime(2023, 7, 15), []),
    ("pozamiatać", "domowe", None, None, None, []),
    ("zrobić zakupy", "inne", None, None, None, ["pomidor", "ogórek", "3.0"])])
def test_add_delete_task(name, cat, desc, exec_date, ddl, subtasks):
    # GIVEN
    priorities = {0: 1, 1: 3, 2: 7}
    suid = Tasker(priorities, 0)
    suid.add_category(cat)
    subtasks = {subtask: False for subtask in subtasks}

    # WHEN
    suid.add_task(name, cat, desc, exec_date, ddl, [])
    suid.get_by_category(cat)
    tasks = suid.current_task_dict
    task = tasks[1]

    suid.delete_task(task.task_id)
    suid.get_by_category(cat)
    empty_tasks = suid.current_task_dict

    suid.delete_category(cat)

    # THEN
    assert task == Task(task_id=1, name=name, cat=cat, desc=desc, exec_date=exec_date, deadline=ddl,
                        is_checked=False, checked_off_date=None,
                        priority=suid._calculate_priority(deadline_date=ddl), subtasks=subtasks)

    assert len(empty_tasks) == 0

def test_add_delete_subtask():
    ...