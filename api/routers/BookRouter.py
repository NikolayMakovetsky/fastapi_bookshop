from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from api.core.validators import BookValidator
from api.database import new_session


from api.models import Book

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
    async def get_by_id(cls, row_id: int) -> BookGetItemSchema | JSONResponse:
        async with new_session() as session:
            row = await session.get(Book, row_id)

            if not row:
                return JSONResponse(status_code=404, content={"title": "Данные не найдены","status": 404,"errors": {}})

            result = BookGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def add_one(cls, data: BookAddSchema) -> BookGetItemSchema | JSONResponse:
        async with new_session() as session:
            book = BookValidateSchema.model_validate(data)
            validator = BookValidator(book, session)
            await validator.validate()

            if not validator.is_valid:
                return JSONResponse(status_code=422, content=validator.response_content())
                # raise HTTPException(status_code=422, detail="Validation errors")

            book_dict = data.model_dump()
            book = Book(**book_dict)

            session.add(book)
            await session.flush()
            await session.commit()
            result = BookGetItemSchema.model_validate(book)
            return result


    @classmethod
    async def update_one(cls, row_id: int, data: BookUpdateSchema) -> BookGetItemSchema | JSONResponse:
        async with new_session() as session:
            book_dict = data.model_dump()
            row = await session.get(Book, row_id)

            if not row:
                return JSONResponse(status_code=404, content={"title": "Данные не найдены","status": 404,"errors": {}})


            print("===", row, type(row))

            for key, value in book_dict.items():
                setattr(row, key, value)

            await session.flush()
            await session.commit()
            result = BookGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def delete_one(cls, row_id: int) ->  None | JSONResponse:
        async with new_session() as session:
            row = await session.get(Book, row_id)

            if not row:
                return JSONResponse(status_code=404, content={"title": "Данные не найдены","status": 404,"errors": {}})

            await session.delete(row)
            await session.flush()
            await session.commit()
