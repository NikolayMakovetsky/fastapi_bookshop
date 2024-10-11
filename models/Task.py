from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from models import ObjBaseModel


class Task(ObjBaseModel):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]