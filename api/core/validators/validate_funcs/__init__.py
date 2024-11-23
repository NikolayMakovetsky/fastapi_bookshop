from api.models import Genre, Author


async def check_genre_id(v: int, session) -> bool:
    row = await session.get(Genre, v)
    if row is None:
        return False
    return True

async def check_author_id(v: int, session) -> bool:
    row = await session.get(Author, v)
    if row is None:
        return False
    return True


async def check_val_gt_zero(v: int, session) -> bool:
    return v > 0


async def check_val_gt_num(v: int, session, num) -> bool:
    return v > num