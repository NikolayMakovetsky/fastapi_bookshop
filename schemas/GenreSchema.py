from pydantic import BaseModel, ConfigDict


class GenreGetListSchema(BaseModel):
    genre_id: int
    name_genre: str

    model_config = ConfigDict(from_attributes=True)

