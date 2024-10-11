from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/ShopDatabase")

new_session = async_sessionmaker(engine, expire_on_commit=False)
