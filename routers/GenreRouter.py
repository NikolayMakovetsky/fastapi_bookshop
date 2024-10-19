from fastapi import APIRouter
from sqlalchemy import select
from database import new_session

from models import Genre
from schemas import GenreGetListSchema, GenreAddSchema, GenreGetItemSchema, GenreUpdateSchema

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


@router.get("/")
async def get_genres() -> list[GenreGetListSchema]:
    genres = await GenreRepository.find_all()
    return genres


@router.get("/{row_id}")
async def get_genre_by_id(row_id: int) -> GenreGetItemSchema:
    genre = await GenreRepository.get_by_id(row_id)
    return genre


@router.post("/", status_code=201)
async def add_genre(genre: GenreAddSchema) -> GenreGetItemSchema:
    genre_item = await GenreRepository.add_one(genre)
    return genre_item


@router.put("/{row_id}")
async def update_genre(row_id: int, genre: GenreUpdateSchema) -> GenreGetItemSchema:
    genre_item = await GenreRepository.update_one(row_id, genre)
    return genre_item


@router.delete("/{row_id}")
async def delete_genre(row_id: int):
    await GenreRepository.delete_one(row_id)


class GenreRepository:

    @classmethod
    async def add_one(cls, data: GenreAddSchema) -> GenreGetItemSchema:
        async with new_session() as session:
            genre_dict = data.model_dump()
            genre = Genre(**genre_dict)
            session.add(genre)
            await session.flush()
            await session.commit()
            result = GenreGetItemSchema.model_validate(genre)
            return result

    @classmethod
    async def find_all(cls) -> list[GenreGetListSchema]:
        async with new_session() as session:
            query = select(Genre).order_by(Genre.name_genre.asc())
            query_res = await session.execute(query)
            rows = query_res.scalars().all()
            result = [GenreGetListSchema.model_validate(row) for row in rows]
            return result

    @classmethod
    async def get_by_id(cls, row_id: int) -> GenreGetItemSchema:
        async with new_session() as session:
            row = await session.get(Genre, row_id)
            result = GenreGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def update_one(cls, row_id: int, data: GenreUpdateSchema) -> GenreGetItemSchema:
        async with new_session() as session:
            genre_dict = data.model_dump()
            row = await session.get(Genre, row_id)
            row.name_genre = genre_dict.get("name_genre")
            await session.flush()
            await session.commit()
            result = GenreGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def delete_one(cls, row_id: int):
        async with new_session() as session:
            row = await session.get(Genre, row_id)
            await session.delete(row)
            await session.flush()
            await session.commit()
