from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select

from api.core.base_validator import BaseValidator
from api.database import new_session


from api.models import Book, Author, Genre

from api.schemas import BookGetListSchema, BookGetItemSchema, BookAddSchema, BookUpdateSchema
from api.schemas.BookSchema import BookValidateSchema

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



@router.put("/{row_id}")
async def update_item(row_id: int, item: BookUpdateSchema) -> BookGetItemSchema:
    updated_item = await BookRepository.update_one(row_id, item)
    return updated_item


@router.delete("/{row_id}")
async def delete_item(row_id: int):
    await BookRepository.delete_one(row_id)



class BookValidator(BaseValidator):
    def __init__(self, item, session):
        super().__init__(item, session)
        self.rule_for("genre_id", lambda x: x.genre_id) \
            .must(val_gt_zero)\
            .message("genre_id: Некорректное значение")\
            .must(genre_id_func)\
            .message("genre_id не найден в справочнике")
        self.rule_for("author_id", lambda x: x.author_id) \
            .must(val_gt_zero) \
            .message("author_id: Некорректное значение") \
            .must(author_id_func)\
            .message("author_id не найден в справочнике")




async def genre_id_func(v: int, session) -> bool:
    row = await session.get(Genre, v)
    if row is None:
        return False
    return True

async def author_id_func(v: int, session) -> bool:
    row = await session.get(Author, v)
    if row is None:
        return False
    return True


async def val_gt_zero(v: int, session) -> bool:
    return v > 0


async def val_gt_num(v: int, session, num) -> bool:
    return v > num


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
    async def add_one(cls, data: BookAddSchema) -> BookGetItemSchema | JSONResponse:
        async with new_session() as session:
            book = BookValidateSchema()
            book.title = data.title
            book.author_id = data.author_id
            book.genre_id = data.genre_id
            book.price = data.price
            book.amount = data.amount

            validator = BookValidator(book, session)
            await validator.validate()
            print("----------------------------------")
            print(f"------{validator.errors=}")


            if validator.errors:
                print("Ошибки валидации")
                print(validator.errors)
                return JSONResponse(status_code=422, content={"message": "Validation errors !!"})
                # raise HTTPException(status_code=422, detail="Validation errors")

            book_dict = data.model_dump()
            book = Book(**book_dict)

            session.add(book)
            await session.flush()
            await session.commit()
            result = BookGetItemSchema.model_validate(book)
            return result


    @classmethod
    async def update_one(cls, row_id: int, data: BookUpdateSchema) -> BookGetItemSchema:
        async with new_session() as session:
            book_dict = data.model_dump()
            row = await session.get(Book, row_id)
            print("===", row, type(row))

            for key, value in book_dict.items():
                setattr(row, key, value)

            await session.flush()
            await session.commit()
            result = BookGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def delete_one(cls, row_id: int):
        async with new_session() as session:
            row = await session.get(Book, row_id)
            await session.delete(row)
            await session.flush()
            await session.commit()
