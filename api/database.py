from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.models import User


# engine = create_async_engine("sqlite+aiosqlite:///bookshop_db.db")

class Singleton:
    instance = None

    def __new__(cls):
        if Singleton.instance is None:
            Singleton.instance = super().__new__(cls)
            Singleton._do_work(Singleton.instance)
        return Singleton.instance

    def _do_work(self):
        engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/bookshop_db2", echo=True)
        db_session = async_sessionmaker(engine, expire_on_commit=False)
        self.session = db_session


new_session = Singleton().session

# engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/bookshop_db2", echo=True)
# new_session = async_sessionmaker(engine, expire_on_commit=False)


# Две эти функции берем для реализации FastapiUsers
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


# Depends нужен чтобы просто через него передать параметры функции)
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
