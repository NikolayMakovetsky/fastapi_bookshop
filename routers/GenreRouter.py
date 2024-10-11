from fastapi import APIRouter
from sqlalchemy import select
from database import new_session

from models import Genre
from schemas import GenreGetListSchema


router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


@router.get("/")
async def get_genres() -> list[GenreGetListSchema]:
    genres = await GenreRepository.find_all()
    return genres


class GenreRepository:
    @classmethod
    async def find_all(cls) -> list[GenreGetListSchema]:
        async with new_session() as session:
            # query = select(Genre).order_by(Genre.name_genre.asc())
            query = select(Genre)\
                .where(Genre.genre_id == 2)\
                .order_by(Genre.name_genre.asc())
            # query = select(Genre)
            # query = select(Genre).filter(Genre.genre_id == 2)
            query_res = await session.execute(query)
            rows = query_res.scalars().all()
            result = [GenreGetListSchema.model_validate(row) for row in rows]
            return result
