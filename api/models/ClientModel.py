from datetime import datetime, timezone

from sqlalchemy import Identity, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP, BIGINT

from api.models import Base


class Client(Base):
    __tablename__ = "client"
    __table_args__ = {"schema": "books"}

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name_client: Mapped[str] = mapped_column(String(length=50), nullable=False)
    city_id: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(length=30), nullable=False)

    user_created: Mapped[int] = mapped_column(default=0, nullable=False)
    date_created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    user_modified: Mapped[int] = mapped_column(default=None, nullable=True)
    date_modified: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    row_version: Mapped[BIGINT] = mapped_column(BIGINT, default=0, nullable=False)
