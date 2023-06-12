from datetime import datetime


def get_category_id(cat_name, engine):
    ...


def by_category(cat_id, engine):
    ...


def by_ddl(deadline: datetime, engine):
    ...


def by_exec_date(execution_date: datetime, engine):
    ...


def unchecked_tasks(engine):
    ...


def by_checked_off_date(checked_off_date: datetime, engine):
    ...