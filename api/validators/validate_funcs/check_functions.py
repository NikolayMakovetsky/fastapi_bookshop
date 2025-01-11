from typing import Any

from sqlalchemy import select
from sqlalchemy.sql import and_

from api.models import Genre, Author, Book
from api.core.logging import logger


async def check_genre_id(item, v: int, session) -> bool:
    row = await session.get(Genre, v)
    if row is None:
        return False
    return True


async def check_author_id(item, v: int, session) -> bool:
    row = await session.get(Author, v)
    if row is None:
        return False
    return True


async def is_unique_name_author(item, v: Any, session) -> bool:
    query = select(Author).where(and_(Author.name_author == v, Author.id != item.id))
    query_res = await session.execute(query)
    rows = query_res.scalars().all()
    if rows:
        return False
    return True


async def is_unique_name_genre(item, v: Any, session) -> bool:
    query = select(Genre).where(and_(Genre.name_genre == v, Genre.id != item.id))
    query_res = await session.execute(query)
    rows = query_res.scalars().all()
    if rows:
        return False
    return True

async def is_unique_book_title(item, v: Any, session) -> bool:
    query = select(Book).where(and_(Book.title == v, Book.id != item.id))
    query_res = await session.execute(query)
    rows = query_res.scalars().all()
    if rows:
        return False
    return True