from typing import Any

from sqlalchemy import select

from api.models import Genre, Author


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
    query = select(Author).where(Author.name_author == v)
    query_res = await session.execute(query)
    rows = query_res.scalars().all()
    if rows:
        return False
    return True
