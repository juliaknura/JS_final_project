from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from program.db_tables import Categories, Tasks


def get_category_id(cat_name, engine):
    with Session(engine) as session:
        query = select(Categories.cat_id).where(Categories.name == cat_name)
        ans = session.execute(query).first()
    return ans


def get_category_name(cat_id, engine):
    with Session(engine) as session:
        query = select(Categories.name).where(Categories.cat_id == cat_id)
        ans = session.execute(query).first()
    return ans


def get_category_list(engine):
    with Session(engine) as session:
        query = select(Categories.cat_id, Categories.name)
        ans = session.execute(query).all()
    return ans


def by_category(cat_id, engine):
    with Session(engine) as session:
        query = select().select_from(Tasks).where(Tasks.cat_id == cat_id)
        ans = session.execute(query).all()
    return ans


def by_ddl(deadline: datetime, engine):
    with Session(engine) as session:
        query = select().select_from(Tasks).where(Tasks.deadline == deadline)
        ans = session.execute(query).all()
    return ans


def by_exec_date(execution_date: datetime, engine):
    with Session(engine) as session:
        query = select().select_from(Tasks).where(Tasks.exec_date == execution_date)
        ans = session.execute(query).all()
    return ans


def unchecked_tasks(engine):
    with Session(engine) as session:
        query = select().select_from(Tasks).where(Tasks.is_checked == False)
        ans = session.execute(query).all()
    return ans


def by_checked_off_date(checked_off_date: datetime, engine):
    with Session(engine) as session:
        query = select().select_from(Tasks).where(Tasks.checked_off_date == checked_off_date)
        ans = session.execute(query).all()
    return ans
