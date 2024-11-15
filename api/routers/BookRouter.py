from fastapi import APIRouter
from sqlalchemy import select
from api.database import new_session

# from api.models import Author
from api.models import Book, Author
from api.routers.AuthorRouter import AuthorRepository
from api.routers.GenreRouter import GenreRepository
# from api.schemas import AuthorGetListSchema, AuthorAddSchema, AuthorGetItemSchema, AuthorUpdateSchema
from api.schemas import BookGetListSchema, BookGetItemSchema, BookAddSchema, BookUpdateSchema

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/")
async def get_items() -> list[BookGetListSchema]:
    items = await BookRepository.find_all()
    return items


@router.get("/{row_id}")
async def get_item_by_id(row_id: int) -> BookGetItemSchema:
    item = await BookRepository.get_by_id(row_id)
    return item


@router.post("/", status_code=201)
async def add_item(item: BookAddSchema) -> BookGetItemSchema:
    added_item = await BookRepository.add_one(item)
    return added_item



# @router.put("/{row_id}")
# async def update_item(row_id: int, item: AuthorUpdateSchema) -> AuthorGetItemSchema:
#     updated_item = await AuthorRepository.update_one(row_id, item)
#     return updated_item
#
#
@router.delete("/{row_id}")
async def delete_item(row_id: int):
    await BookRepository.delete_one(row_id)


# class BookValidator:
#
#     @classmethod
#     async def check_added_item(cls, item) -> bool:
#         async with new_session() as session:
#             item_dict = item.model_dump()
#             author = await AuthorRepository.get_by_id(item_dict.get('author_id'))
#             genre = await GenreRepository.get_by_id(item_dict.get('genre_id'))
#             if author and genre:
#                 return True
#             return False




class BookRepository:


    @classmethod
    async def find_all(cls) -> list[BookGetListSchema]:
        async with new_session() as session:
            query = select(Book).order_by(Book.title.asc())
            query_res = await session.execute(query)
            rows = query_res.scalars().all()
            result = [BookGetListSchema.model_validate(row) for row in rows]
            return result

    @classmethod
    async def get_by_id(cls, row_id: int) -> BookGetItemSchema:
        async with new_session() as session:
            row = await session.get(Book, row_id)
            result = BookGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def add_one(cls, data: BookAddSchema) -> BookGetItemSchema | dict:
        async with new_session() as session:
            book_dict = data.model_dump()
            book = Book(**book_dict)

            query = select(Author).where(Author.id == book_dict.get("author_id"))
            query_res = await session.execute(query)
            print("=============")
            print(book_dict.get("author_id"))
            print(query)
            print(query_res)

            session.add(book)
            await session.flush()
            await session.commit()
            result = BookGetItemSchema.model_validate(book)
            return result

    # @classmethod
    # async def update_one(cls, row_id: int, data: AuthorUpdateSchema) -> AuthorGetItemSchema:
    #     async with new_session() as session:
    #         author_dict = data.model_dump()
    #         row = await session.get(Author, row_id)
    #
    #         for key, value in author_dict.items():
    #             setattr(row, key, value)
    #
    #         await session.flush()
    #         await session.commit()
    #         result = AuthorGetItemSchema.model_validate(row)
    #         return result
    #
    @classmethod
    async def delete_one(cls, row_id: int):
        async with new_session() as session:
            row = await session.get(Book, row_id)
            await session.delete(row)
            await session.flush()
            await session.commit()
