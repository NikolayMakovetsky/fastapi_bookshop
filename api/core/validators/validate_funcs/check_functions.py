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
