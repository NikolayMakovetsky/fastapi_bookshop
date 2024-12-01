from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.dialects.postgresql import BIGINT


class BookBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = "Test title"
    author_id: int = 0
    genre_id: int = 0
    price: float = 0.00
    amount: int = 0


class BookAddSchema(BookBaseSchema):
    pass

class BookUpdateSchema(BookBaseSchema):
    row_version: int = None


class BookDeleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    row_version: int = 0


class BookValidateSchema(BookUpdateSchema):
    pass


class BookGetItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author_id: int
    genre_id: int
    price: float
    amount: int

    user_created: int
    date_created: datetime
    user_modified: int | None
    date_modified: datetime | None
    row_version: int  # BIGINT


class BookGetListSchema(BookGetItemSchema):
    pass
