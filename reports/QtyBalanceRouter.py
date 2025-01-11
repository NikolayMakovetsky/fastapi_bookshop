
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.functions import coalesce

from api.core.database import db_session
from api.core.dependencies import get_user_settings

from api.models import Book, BuyBook, Author, Genre

router = APIRouter(
    prefix="/reports/qty_balance",
    tags=["Reports"],
    dependencies=[Depends(get_user_settings)]
)


class QtyBalanceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author_name: str
    genre_name: str
    price: float
    qty: int
    qty_sold: int
    qty_balance: int


@router.get("/")
async def get_qty_balance(current_user_settings = Depends(get_user_settings)):  #  -> list[QtyBalanceSchema]
    lang = current_user_settings['current_language']
    items = await ReportRepository.find_all(lang)
    return items


class ReportRepository:

# select a.id, a.title, a.price, a.qty AS qty_on_hand, COALESCE(b.qty,0) AS qty_sold, a.qty-COALESCE(b.qty,0) AS stock_balance from books.book a
# left join (select book_id, sum(qty) as qty from books.buy_book group by book_id) b
# on b.book_id = a.id
# where a.qty-COALESCE(b.qty,0) > 0

    @classmethod
    async def find_all(cls, lang: str):  #  -> list[QtyBalanceSchema]
        async with db_session() as session:
            buy_book = select(BuyBook.book_id,
                             func.sum(BuyBook.qty).label('qty')
                             ).group_by(BuyBook.book_id).subquery()

            query = select(Book.id,
                           Book.title,
                           Author.name_author.label('author_name'),
                           Genre.name_genre.label('genre_name'),
                           Book.price,
                           Book.qty,
                           coalesce(buy_book.c.qty,0).label('qty_sold'),
                           (Book.qty - coalesce(buy_book.c.qty,0)).label('qty_balance')) \
                .outerjoin(buy_book, Book.id == buy_book.c.book_id) \
                .join(Author, Book.author_id == Author.id) \
                .join(Genre, Book.genre_id == Genre.id) \
                .where((Book.qty - coalesce(buy_book.c.qty,0)) > 0) \
                .order_by(Book.title.asc())

            query_res = await session.execute(query)

            result = []
            for row in query_res:
                result.append(QtyBalanceSchema.model_validate(row))

            return result