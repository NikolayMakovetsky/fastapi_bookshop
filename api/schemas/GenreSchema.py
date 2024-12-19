from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GenreBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name_genre: str = "Genre"


class GenreAddSchema(GenreBaseSchema):
    pass

class GenreUpdateSchema(GenreBaseSchema):
    row_version: int = None


class GenreDeleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    row_version: int = 0


class GenreValidateSchema(GenreUpdateSchema):
    pass


class GenreGetItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = 0
    name_genre: str = ""

    user_created: int = 0
    date_created: datetime | None = None
    user_modified: int | None = None
    date_modified: datetime | None = None
    row_version: int  = 0  # BIGINT


class GenreGetListSchema(GenreGetItemSchema):
    pass
