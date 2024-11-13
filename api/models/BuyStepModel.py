from datetime import datetime, timezone

from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP, BIGINT, DATE

from api.models import Base


class BuyStep(Base):
    __tablename__ = "buy_step"
    __table_args__ = {"schema": "books"}

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    buy_id: Mapped[int] = mapped_column(nullable=False)
    step_id: Mapped[int] = mapped_column(nullable=False)
    date_step_beg: Mapped[datetime] = mapped_column(DATE, nullable=True)
    date_step_end: Mapped[datetime] = mapped_column(DATE, nullable=True)

    user_created: Mapped[int] = mapped_column(default=0, nullable=False)
    date_created: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    user_modified: Mapped[int] = mapped_column(default=None, nullable=True)
    date_modified: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)
    row_version: Mapped[BIGINT] = mapped_column(BIGINT, default=0, nullable=False)
