from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name_author: str = "Test author"


class AuthorAddSchema(AuthorBaseSchema):
    pass

class AuthorUpdateSchema(AuthorBaseSchema):
    pass


class AuthorGetItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_author: str

    user_created: int
    date_created: datetime
    # user_modified: int = None
    # date_modified: datetime = None
    row_version: int  # BIGINT


class AuthorGetListSchema(AuthorGetItemSchema):
    pass
