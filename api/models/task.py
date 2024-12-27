from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column("title")
    due_date: Mapped[date] = mapped_column("due_date", nullable=True)

    done = relationship("Done", back_populates="task", cascade="delete")


class Done(Base):
    __tablename__ = "dones"

    id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)

    task = relationship("Task", back_populates="done")
