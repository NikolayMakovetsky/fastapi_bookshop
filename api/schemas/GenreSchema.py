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

    genre_id: int
    name_genre: str


class GenreGetListSchema(GenreGetItemSchema):
    pass
