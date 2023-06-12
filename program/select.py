from datetime import datetime


def get_category_id(cat_name):
    ...


def by_category(cat_id):
    ...


def by_ddl(deadline: datetime):
    ...


def by_exec_date(execution_date: datetime):
    ...


def unchecked_tasks():
    ...


def by_checked_off_date(checked_off_date: datetime):
    ...