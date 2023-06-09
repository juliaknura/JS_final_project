import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref

db_file_name = "app_data"
db = f"sqlite:///{db_file_name}.db"


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    cat_id: Mapped[int] = mapped_column(ForeignKey("categories.cat_id"))
    task_desc: Mapped[Optional[str]]
    exec_date: Mapped[Optional[datetime.datetime]]
    deadline: Mapped[Optional[datetime.datetime]]
    is_checked: Mapped[bool]
    checked_off_date: Mapped[Optional[datetime.datetime]]

    category: Mapped["Categories"] = relationship(back_populates="tasks")
    subtasks: Mapped[List["Subtasks"]] = relationship(back_populates="parent_task",
                                                      cascade="all, delete-orphan")

class Categories(Base):
    __tablename__ = "categories"

    cat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

    tasks: Mapped["Tasks"] = relationship(back_populates="category")


class Subtasks(Base):
    __tablename__ = "subtasks"

    name: Mapped[str] = mapped_column()
    is_checked: Mapped[bool]
    parent_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.task_id"))

    parent_task: Mapped["Tasks"] = relationship(back_populates="subtasks")
    __mapper_args__ = {"primary_key": [parent_task_id, name]}
