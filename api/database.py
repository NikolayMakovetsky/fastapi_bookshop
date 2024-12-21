from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.core.logging import logger
from api.models import User

# engine = create_async_engine("sqlite+aiosqlite:///bookshop_db.db")
# db_connection_string = "postgresql+asyncpg://postgres:postgres@localhost:5432/bookshop_db2"

DB_DRIVER = "postgresql+asyncpg"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bookshop_db2"
DB_USER = "postgres"
DB_PASS = "postgres"


class AppSession:
    instance = None

    def __new__(cls, db_driver, db_host, db_port, db_name, db_user, db_pass):
        if AppSession.instance is None:
            AppSession.instance = super().__new__(cls)
            AppSession._do_work(AppSession.instance, db_driver, db_host, db_port, db_name, db_user, db_pass)
        return AppSession.instance

    def _do_work(self, db_driver, db_host, db_port, db_name, db_user, db_pass):
        db_connection_string = f"{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_async_engine(db_connection_string)
        database_session = async_sessionmaker(engine, expire_on_commit=False)
        self.engine = engine
        self.db_session = database_session
        self.db_driver = db_driver
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user


app_session = AppSession(DB_DRIVER, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
db_session = app_session.db_session


# FastapiUsers settings
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_session() as session:
        yield session


# FastapiUsers settings
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
