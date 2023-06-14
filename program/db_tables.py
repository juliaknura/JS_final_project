import datetime

from sqlalchemy import ForeignKey, create_engine
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


class Categories(Base):
    __tablename__ = "categories"

    cat_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    tasks: Mapped["Tasks"] = relationship(back_populates="category")