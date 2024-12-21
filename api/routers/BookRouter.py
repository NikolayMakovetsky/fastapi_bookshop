from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from api.core.localizators import validation_problem
from api.core.logging import logger
from api.core.validators import BookValidator
from api.database import db_session

from api.models import Book, User

from api.schemas import (BookGetListSchema, BookGetItemSchema, BookAddSchema,
                         BookUpdateSchema, BookValidateSchema, BookDeleteSchema)
from auth.user import current_active_user

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/")
async def get_items(user: User = Depends(current_active_user)) -> list[BookGetListSchema]:
    items = await BookRepository.find_all()
    return items


@router.get("/{row_id}")
async def get_item_by_id(row_id: int, user: User = Depends(current_active_user)) -> BookGetItemSchema:
    item = await BookRepository.get_by_id(row_id, user)
    return item


@router.post("/", status_code=201)
async def add_item(item: BookAddSchema, user: User = Depends(current_active_user)) -> BookGetItemSchema:
    added_item = await BookRepository.add_one(item, user)
    return added_item


@router.put("/{row_id}")
async def update_item(row_id: int, item: BookUpdateSchema,
                      user: User = Depends(current_active_user)) -> BookGetItemSchema:
    updated_item = await BookRepository.update_one(row_id, item, user)
    return updated_item


@router.delete("/{row_id}")
async def delete_item(row_id: int, item: BookDeleteSchema, user: User = Depends(current_active_user)) -> dict:
    res = await BookRepository.delete_one(row_id, item)
    return res


class BookRepository:

    @classmethod
    async def find_all(cls) -> list[BookGetListSchema]:
        async with db_session() as session:
            query = select(Book).order_by(Book.title.asc())
            query_res = await session.execute(query)
            rows = query_res.scalars().all()
            result = [BookGetListSchema.model_validate(row) for row in rows]
            return result

    @classmethod
    async def get_by_id(cls, row_id: int, user: User) -> BookGetItemSchema | JSONResponse:

        if row_id == 0:
            book = BookGetItemSchema()
            book.user_created = user.id
            book.date_created = datetime.now(timezone.utc)
            return book

        async with db_session() as session:
            row = await session.get(Book, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            result = BookGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def add_one(cls, data: BookAddSchema, user: User) -> BookGetItemSchema | JSONResponse:
        async with db_session() as session:
            book = BookValidateSchema.model_validate(data)
            validator = BookValidator(book, session)
            await validator.validate()

            if not validator.is_valid:
                return validation_problem(status=HTTPStatus.UNPROCESSABLE_ENTITY, content=validator.response_content())

            row = Book()
            book_dict = book.model_dump()
            for key, value in book_dict.items():
                if hasattr(row, key):
                    setattr(row, key, value)

            row.user_created = user.id
            row.date_created = datetime.now(timezone.utc)

            session.add(row)
            try:
                await session.flush()
                await session.commit()
            except SQLAlchemyError as e:
                # func for logger
                return validation_problem(status=HTTPStatus.CONFLICT)

            result = BookGetItemSchema.model_validate(row)

            return result

    @classmethod
    async def update_one(cls, row_id: int, data: BookUpdateSchema, user: User) -> BookGetItemSchema | JSONResponse:
        async with db_session() as session:
            row = await session.get(Book, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            if row.row_version != data.row_version:
                return validation_problem(status=HTTPStatus.PRECONDITION_FAILED)

            book = BookValidateSchema.model_validate(row)
            book = book.model_validate(data)  # затирает данные
            book.id = row.id

            validator = BookValidator(book, session)
            await validator.validate()

            if not validator.is_valid:
                return validation_problem(status=HTTPStatus.UNPROCESSABLE_ENTITY, content=validator.response_content())

            book_dict = book.model_dump()
            for key, value in book_dict.items():
                if hasattr(row, key):
                    setattr(row, key, value)

            row.user_modified = user.id
            row.date_modified = datetime.now(timezone.utc)
            row.row_version += 1

            try:
                await session.flush()
                await session.commit()
            except SQLAlchemyError as e:
                # func for logger
                err = str(e.__dict__['orig'])  # + 'statement'
                logger.error(err)
                return validation_problem(status=HTTPStatus.CONFLICT)

            result = BookGetItemSchema.model_validate(row)

            return result

    @classmethod
    async def delete_one(cls, row_id: int, data: BookDeleteSchema) -> dict | JSONResponse:
        async with db_session() as session:
            row = await session.get(Book, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            if row.row_version != data.row_version:
                return validation_problem(status=HTTPStatus.PRECONDITION_FAILED)

            await session.delete(row)
            try:
                await session.flush()
                await session.commit()
            except SQLAlchemyError as e:
                # func for logger
                return validation_problem(status=HTTPStatus.CONFLICT)

            return {}
