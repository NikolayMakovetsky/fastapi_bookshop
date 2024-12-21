from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from api.core.localizators import validation_problem
from api.core.logging import logger
from api.core.validators import AuthorValidator
from api.database import db_session

from api.models import Author
from api.schemas import (AuthorGetListSchema, AuthorAddSchema, AuthorGetItemSchema,
                         AuthorUpdateSchema, AuthorDeleteSchema, AuthorValidateSchema)

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
async def delete_item(row_id: int, item: AuthorDeleteSchema) -> dict:
    res = await AuthorRepository.delete_one(row_id, item)
    return res



class AuthorRepository:

    @classmethod
    async def find_all(cls) -> list[AuthorGetListSchema]:
        async with db_session() as session:
            query = select(Author).order_by(Author.name_author.asc())
            query_res = await session.execute(query)
            rows = query_res.scalars().all()
            result = [AuthorGetListSchema.model_validate(row) for row in rows]
            return result

    @classmethod
    async def get_by_id(cls, row_id: int) -> AuthorGetItemSchema | JSONResponse:

        if row_id == 0:
            author = AuthorGetItemSchema()
            author.user_created = author.id  # ???
            author.date_created = datetime.now(timezone.utc)
            return author

        async with db_session() as session:
            row = await session.get(Author, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            result = AuthorGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def add_one(cls, data: AuthorAddSchema) -> AuthorGetItemSchema | JSONResponse:
        async with db_session() as session:
            author = AuthorValidateSchema.model_validate(data)
            validator = AuthorValidator(author, session)
            await validator.validate()

            if not validator.is_valid:
                return validation_problem(status=HTTPStatus.UNPROCESSABLE_ENTITY,
                                          content=validator.response_content())

            row = Author()
            author_dict = author.model_dump()
            for key, value in author_dict.items():
                if hasattr(row, key):
                    setattr(row, key, value)

            # row.user_created = user.id
            row.date_created = datetime.now(timezone.utc)

            session.add(row)
            try:
                await session.flush()
                await session.commit()
            except SQLAlchemyError as e:
                # func for logger
                return validation_problem(status=HTTPStatus.CONFLICT)

            result = AuthorGetItemSchema.model_validate(row)

            return result

    @classmethod
    async def update_one(cls, row_id: int, data: AuthorUpdateSchema) -> AuthorGetItemSchema | JSONResponse:
        async with db_session() as session:
            row = await session.get(Author, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            if row.row_version != data.row_version:
                return validation_problem(status=HTTPStatus.PRECONDITION_FAILED)

            author = AuthorValidateSchema.model_validate(row)
            author = author.model_validate(data)

            validator = AuthorValidator(author, session)
            await validator.validate()

            if not validator.is_valid:
                return validation_problem(status=HTTPStatus.UNPROCESSABLE_ENTITY,
                                          content=validator.response_content())

            author_dict = author.model_dump()
            for key, value in author_dict.items():
                if hasattr(row, key):
                    setattr(row, key, value)

            # row.user_modified = user.id
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

            result = AuthorGetItemSchema.model_validate(row)

            return result

    @classmethod
    async def delete_one(cls, row_id: int, data: AuthorDeleteSchema) -> dict | JSONResponse:
        async with db_session() as session:
            row = await session.get(Author, row_id)

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

