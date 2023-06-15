import datetime

import pytest as pytest
from program.Task import Task
from program.Tasker import Tasker


def test_add_category():
    #GIVEN
    priorities = {0: 1, 1: 3, 2: 7}
    suid = Tasker(priorities, 0)
    name = "tajna_kategoria"

    #WHEN
    suid.add_category(name)
    categories = suid.category_list()

    #THEN
    assert categories[0] == name


@pytest.mark.parametrize("name, cat, desc, exec_date, ddl", [
    ("odkurzyć", "domowe", "opis opis", datetime.datetime(2023, 7, 13), datetime.datetime(2023, 7, 15))])
def test_add_task(name, cat, desc, exec_date, ddl):
    # GIVEN
    priorities = {0: 1, 1: 3, 2: 7}
    suid = Tasker(priorities, 0)
    suid.add_category(cat)

    # WHEN
    suid.add_task(name, cat, desc, exec_date, ddl, [])
    suid.get_by_category(cat)
    tasks = suid.current_task_dict
    task = tasks[1]

    # THEN
    assert task == Task(task_id=1, name=name, cat=cat, desc=desc, exec_date=exec_date, deadline=ddl,
                               is_checked=False, checked_off_date=None,
                               priority=suid._calculate_priority(deadline_date=ddl), subtasks={})
