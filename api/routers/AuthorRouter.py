from fastapi import APIRouter
from sqlalchemy import select
from api.database import new_session

from api.models import Author
from api.schemas import AuthorGetListSchema, AuthorAddSchema, AuthorGetItemSchema, AuthorUpdateSchema

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


@router.get("/")
async def get_items() -> list[AuthorGetListSchema]:
    items = await AuthorRepository.find_all()
    return items


@router.get("/{row_id}")
async def get_item_by_id(row_id: int) -> AuthorGetItemSchema:
    item = await AuthorRepository.get_by_id(row_id)
    return item


@router.post("/", status_code=201)
async def add_item(item: AuthorAddSchema) -> AuthorGetItemSchema:
    added_item = await AuthorRepository.add_one(item)
    return added_item


@router.put("/{row_id}")
async def update_item(row_id: int, item: AuthorUpdateSchema) -> AuthorGetItemSchema:
    updated_item = await AuthorRepository.update_one(row_id, item)
    return updated_item


@router.delete("/{row_id}")
async def delete_item(row_id: int):
    await AuthorRepository.delete_one(row_id)


class AuthorRepository:


    @classmethod
    async def find_all(cls) -> list[AuthorGetListSchema]:
        async with new_session() as session:
            query = select(Author).order_by(Author.name_author.asc())
            query_res = await session.execute(query)
            rows = query_res.scalars().all()
            result = [AuthorGetListSchema.model_validate(row) for row in rows]
            return result

    @classmethod
    async def get_by_id(cls, row_id: int) -> AuthorGetItemSchema:
        async with new_session() as session:
            row = await session.get(Author, row_id)
            result = AuthorGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def add_one(cls, data: AuthorAddSchema) -> AuthorGetItemSchema:
        async with new_session() as session:
            author_dict = data.model_dump()
            author = Author(**author_dict)
            session.add(author)
            await session.flush()
            await session.commit()
            result = AuthorGetItemSchema.model_validate(author)
            return result

    @classmethod
    async def update_one(cls, row_id: int, data: AuthorUpdateSchema) -> AuthorGetItemSchema:
        async with new_session() as session:
            author_dict = data.model_dump()
            row = await session.get(Author, row_id)

            for key, value in author_dict.items():
                setattr(row, key, value)

            await session.flush()
            await session.commit()
            result = AuthorGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def delete_one(cls, row_id: int):
        async with new_session() as session:
            row = await session.get(Author, row_id)
            await session.delete(row)
            await session.flush()
            await session.commit()
