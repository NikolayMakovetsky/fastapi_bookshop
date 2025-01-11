from fastapi import APIRouter, Depends

from sqlalchemy import select, exists
from pydantic import BaseModel, ConfigDict

from api.core.database import db_session
from api.core.dependencies import get_user_settings

from api.models import Book, BuyBook, Author, Genre


class BooksThatWasNotSoldSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author_name: str
    genre_name: str
    price: float
    qty: int


router = APIRouter(
    prefix="/reports/books_that_was_not_sold",
    tags=["Reports"],
    dependencies=[Depends(get_user_settings)]
)


@router.get("/")
async def get_books_that_was_not_sold(current_user_settings=Depends(get_user_settings)) \
        -> list[BooksThatWasNotSoldSchema]:
    lang = current_user_settings['current_language']
    items = await ReportRepository.find_all(lang)
    return items


class ReportRepository:

    @classmethod
    async def find_all(cls, lang: str) -> list[BooksThatWasNotSoldSchema]:
        async with db_session() as session:
            query = select(Book.id,
                           Book.title,
                           Author.name_author.label('author_name'),
                           Genre.name_genre.label('genre_name'),
                           Book.price,
                           Book.qty) \
                .join(Author, Book.author_id == Author.id) \
                .join(Genre, Book.genre_id == Genre.id) \
                .filter(~exists().where(BuyBook.book_id == Book.id)) \
                .order_by(Book.title.asc())

            query_res = await session.execute(query)

            result = []
            for row in query_res:
                result.append(BooksThatWasNotSoldSchema.model_validate(row))

            return result
