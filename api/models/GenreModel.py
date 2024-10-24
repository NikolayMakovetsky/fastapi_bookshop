from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column
from api.models import Base


class Genre(Base):
    __tablename__ = "genre"
    __table_args__ = {"schema": "books"}

    # genre_id: Mapped[int] = mapped_column(Sequence('genre_genre_id_seq', start=1, increment=1), Identity(),primary_key=True)
    genre_id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name_genre: Mapped[str]
