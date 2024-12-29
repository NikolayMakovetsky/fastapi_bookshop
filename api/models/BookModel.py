from datetime import datetime, timezone

from sqlalchemy import Identity, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP, BIGINT

from api.models import Base


class Book(Base):
    __tablename__ = "book"
    __table_args__ = {"schema": "books"}

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    title: Mapped[str]  = mapped_column(String(length=50), nullable=False)
    author_id: Mapped[int]  = mapped_column(nullable=False)
    genre_id: Mapped[int]  = mapped_column(nullable=False)
    price: Mapped[float]  = mapped_column(Numeric(10,2), nullable=False)
    qty: Mapped[int]  = mapped_column(nullable=False)

    user_created: Mapped[int] = mapped_column(default=0, nullable=False)
    date_created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    user_modified: Mapped[int] = mapped_column(default=None, nullable=True)
    date_modified: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    row_version: Mapped[BIGINT] = mapped_column(BIGINT, default=0, nullable=False)
