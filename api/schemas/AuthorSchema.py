from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name_author: str = "Ivanov Ivan"


class AuthorAddSchema(AuthorBaseSchema):
    pass

class AuthorUpdateSchema(AuthorBaseSchema):
    row_version: int = None


class AuthorDeleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    row_version: int = 0


class AuthorValidateSchema(AuthorUpdateSchema):
    id: int = 0


class AuthorGetItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = 0
    name_author: str = ""

    user_created: int = 0
    date_created: datetime | None = None
    user_modified: int | None = None
    date_modified: datetime | None = None
    row_version: int  = 0  # BIGINT


class AuthorGetListSchema(AuthorGetItemSchema):
    pass
