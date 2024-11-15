from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.dialects.postgresql import BIGINT


class BookBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = "Test title"
    author_id: int = "0"
    genre_id: int = "0"
    price: float = 0.00
    amount: int = 0

    # @field_validator()
    # @classmethod
    # def validation_func(cls, v: str):
    #     if len(v) < 3:
    #         raise ValueError("title should includes 3 or more letters")
    #     return v

class BookAddSchema(BookBaseSchema):
    pass

class BookUpdateSchema(BookBaseSchema):
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
