from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from api.core.localizators import validation_problem
from api.core.logging import logger
from api.core.validators import GenreValidator
from api.database import db_session

from api.models import Genre, User
from api.schemas import (GenreGetListSchema, GenreGetItemSchema, GenreAddSchema,
                         GenreUpdateSchema, GenreDeleteSchema, GenreValidateSchema)
from auth.user import current_active_user

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


@router.get("/")
async def get_items(user: User = Depends(current_active_user)) -> list[GenreGetListSchema]:
    items = await GenreRepository.find_all()
    return items


@router.get("/{row_id}")
async def get_item_by_id(row_id: int, user: User = Depends(current_active_user)) -> GenreGetItemSchema:
    item = await GenreRepository.get_by_id(row_id, user)
    return item


@router.post("/", status_code=201)
async def add_item(item: GenreAddSchema, user: User = Depends(current_active_user)) -> GenreGetItemSchema:
    added_item = await GenreRepository.add_one(item, user)
    return added_item


@router.put("/{row_id}")
async def update_item(row_id: int, item: GenreUpdateSchema,
                      user: User = Depends(current_active_user)) -> GenreGetItemSchema:
    updated_item = await GenreRepository.update_one(row_id, item, user)
    return updated_item


@router.delete("/{row_id}")
async def delete_item(row_id: int, user: User = Depends(current_active_user)) -> dict:
    res = await GenreRepository.delete_one(row_id)
    return res


class GenreRepository:

    @classmethod
    async def find_all(cls) -> list[GenreGetListSchema]:
        async with db_session() as session:
            query = select(Genre).order_by(Genre.name_genre.asc())
            query_res = await session.execute(query)
            rows = query_res.scalars().all()
            result = [GenreGetListSchema.model_validate(row) for row in rows]
            return result

    @classmethod
    async def get_by_id(cls, row_id: int, user: User) -> GenreGetItemSchema | JSONResponse:

        if row_id == 0:
            genre = GenreGetItemSchema()
            genre.user_created = user.id
            genre.date_created = datetime.now(timezone.utc)
            return genre

        async with db_session() as session:
            row = await session.get(Genre, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            result = GenreGetItemSchema.model_validate(row)
            return result

    @classmethod
    async def add_one(cls, data: GenreAddSchema, user: User) -> GenreGetItemSchema | JSONResponse:
        async with db_session() as session:
            genre = GenreValidateSchema.model_validate(data)
            validator = GenreValidator(genre, session)
            await validator.validate()

            if not validator.is_valid:
                return validation_problem(status=HTTPStatus.UNPROCESSABLE_ENTITY,
                                          content=validator.response_content())

            row = Genre()
            genre_dict = genre.model_dump()
            for key, value in genre_dict.items():
                if hasattr(row, key):
                    setattr(row, key, value)

            row.id = None
            row.user_created = user.id
            row.date_created = datetime.now(timezone.utc)
            row.row_version = 0

            session.add(row)
            try:
                await session.flush()
                await session.commit()
            except SQLAlchemyError as e:
                # func for logger
                return validation_problem(status=HTTPStatus.CONFLICT)

            result = GenreGetItemSchema.model_validate(row)

            return result

    @classmethod
    async def update_one(cls, row_id: int, data: GenreUpdateSchema, user: User) -> GenreGetItemSchema | JSONResponse:
        async with db_session() as session:
            row = await session.get(Genre, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            if row.row_version != data.row_version:
                return validation_problem(status=HTTPStatus.PRECONDITION_FAILED)

            genre = GenreValidateSchema.model_validate(row)
            genre = genre.model_validate(data)
            genre.id = row.id

            validator = GenreValidator(genre, session)
            await validator.validate()

            if not validator.is_valid:
                return validation_problem(status=HTTPStatus.UNPROCESSABLE_ENTITY,
                                          content=validator.response_content())

            genre_dict = genre.model_dump()
            for key, value in genre_dict.items():
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

            result = GenreGetItemSchema.model_validate(row)

            return result

    @classmethod
    async def delete_one(cls, row_id: int) -> dict | JSONResponse:
        async with db_session() as session:
            row = await session.get(Genre, row_id)

            if not row:
                return validation_problem(status=HTTPStatus.NOT_FOUND)

            await session.delete(row)
            try:
                await session.flush()
                await session.commit()
            except SQLAlchemyError as e:
                # func for logger
                return validation_problem(status=HTTPStatus.CONFLICT)

            return {}
