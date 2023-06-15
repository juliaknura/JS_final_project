import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

db_name = "app_data"


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    cat_id: Mapped[int] = mapped_column(ForeignKey("categories.cat_id"))
    task_desc: Mapped[str]
    exec_date: Mapped[datetime.datetime]
    deadline: Mapped[datetime.datetime]
    is_checked: Mapped[bool]
    checked_off_date: Mapped[datetime.datetime]

    category: Mapped["Categories"] = relationship(back_populates="tasks")
    subtasks: Mapped[List["Subtasks"]] = relationship(back_populates="parent", cascade="all, delete")

class Categories(Base):
    __tablename__ = "categories"

    cat_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    tasks: Mapped["Tasks"] = relationship(back_populates="category")

class Subtasks(Base):
    __tablename__ = "subtasks"

    name: Mapped[str]
    is_checked: Mapped[bool]
    parent_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.task_id"))

    parent: Mapped["Tasks"] = relationship(back_populates="subtasks")
    __mapper_args__ = {"primary_key": [parent_task_id, name]}