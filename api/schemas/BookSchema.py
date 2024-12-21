from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.dialects.postgresql import BIGINT


class BookBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = "Test title"
    author_id: int = 0
    genre_id: int = 0
    price: float = 0.0
    amount: int = 0


class BookAddSchema(BookBaseSchema):
    pass

class BookUpdateSchema(BookBaseSchema):
    row_version: int = None


class BookDeleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    row_version: int = 0


class BookValidateSchema(BookUpdateSchema):
    id: int = 0


class BookGetItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = 0
    title: str = ""
    author_id: int | None = None
    genre_id: int | None = None
    price: float = 0.0
    amount: int = 0

    user_created: int = 0
    date_created: datetime | None = None
    user_modified: int | None = None
    date_modified: datetime | None = None
    row_version: int  = 0  # BIGINT


class BookGetListSchema(BookGetItemSchema):
    pass
