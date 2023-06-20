from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from program.db_tables import Categories, Tasks, Subtasks


def get_category_id(cat_name, engine):
    """Returns (id, )"""
    with Session(engine) as session:
        query = select(Categories.cat_id).where(Categories.name == cat_name)
        ans = session.execute(query).first()
    return ans


def get_category_name(cat_id, engine):
    """Returns (name, )"""
    with Session(engine) as session:
        query = select(Categories.name).where(Categories.cat_id == cat_id)
        ans = session.execute(query).first()
    return ans


def get_category_list(engine):
    """Returns a list of (id, name, ) tuples"""
    with Session(engine) as session:
        query = select(Categories.cat_id, Categories.name)
        ans = session.execute(query).all()
    return ans


def by_category(cat_id, engine):
    """Returns a list of unchecked tasks with given category"""
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.cat_id == cat_id).where(Tasks.is_checked == False)
        ans = session.execute(query).all()
    return ans


def by_category_all(cat_id, engine):
    """Returns a list of all tasks with given category"""
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.cat_id == cat_id)
        ans = session.execute(query).all()
    return ans


def by_ddl(deadline: datetime, engine):
    """Returns a list of unchecked tasks with given deadline"""
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.deadline == deadline).where(Tasks.is_checked == False)
        ans = session.execute(query).all()
    return ans


def by_exec_date(execution_date: datetime, engine):
    """Returns a list of unchecked tasks with given execution date"""
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.exec_date == execution_date).where(Tasks.is_checked == False)
        ans = session.execute(query).all()
    return ans


def unchecked_tasks(engine):
    """Returns a list of tasks that haven't been checked off"""
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.is_checked == False)
        ans = session.execute(query).all()
    return ans


def checked_off_tasks(engine):
    """Returns a list of tasks that have been checked off"""
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.is_checked == True)
        ans = session.execute(query).all()
    return ans


def by_checked_off_date(checked_off_date: datetime, engine):
    """Returns a list of tuples with tasks that have been checked off at given day"""
    with Session(engine) as session:
        query = select(Tasks).where(Tasks.checked_off_date == checked_off_date)
        ans = session.execute(query).all()
    return ans


def get_subtasks(task_id, engine):
    """Returns a list of (name, is_checked, ) tuples with subtasks for a given task"""
    with Session(engine) as session:
        query = select(Subtasks.name, Subtasks.is_checked).where(Subtasks.parent_task_id == task_id)
        ans = session.execute(query).all()
    return ans
