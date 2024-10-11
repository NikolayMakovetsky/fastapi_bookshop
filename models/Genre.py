from typing import Optional

from sqlalchemy import Sequence
from sqlalchemy.orm import Mapped, mapped_column
from models import ObjBaseModel


class Genre(ObjBaseModel):
    __tablename__ = "genre"
    __table_args__ = {"schema": "books"}

    genre_id: Mapped[int] = mapped_column(Sequence('genre_genre_id_seq', start=1, increment=1), primary_key=True)
    name_genre: Mapped[str]
