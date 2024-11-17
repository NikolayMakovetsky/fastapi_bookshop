from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GenreBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name_genre: str = "Test genre"


class GenreAddSchema(GenreBaseSchema):
    pass

class GenreUpdateSchema(GenreBaseSchema):
    pass


class GenreGetItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_genre: str

    user_created: int
    date_created: datetime
    user_modified: int | None
    date_modified: datetime | None
    row_version: int  # BIGINT


class GenreGetListSchema(GenreGetItemSchema):
    pass
