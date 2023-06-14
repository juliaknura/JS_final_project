import datetime

import pytest as pytest
from program.Task import Task

@pytest.mark.parametrize("task_id, name, cat, desc, exec_date, deadline, priority, is_checked, checked_off_date", [
    (14, "odkurzyć kuchnię", 2, "pamiętaj o kątach i miejscami pod szafkami", datetime.datetime(2023, 5, 10), datetime.datetime(2023, 6, 15), True, datetime.datetime(2023, 6, 13), 1),
])
def test_tasker_init(task_id, name, cat, desc, exec_date, deadline, is_checked, checked_off_date, priority):
    #WHEN
    suid = Task(task_id, name, cat, desc, exec_date, deadline, is_checked, checked_off_date, priority)

    #THEN
    assert suid.task_id == task_id
    assert suid.name == name
    assert suid.cat == cat
    assert suid.desc == desc
    assert suid.exec_date == exec_date
    assert suid.deadline == deadline
    assert suid.priority == priority
    assert suid.is_checked == is_checked
    assert suid.checked_off_date == checked_off_date
    assert suid.priority == priority