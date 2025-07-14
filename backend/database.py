from sqlmodel import create_async_engine, AsyncSession, SQLModel
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///backend/database.db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def init_db():
    async with engine.begin() as conn:
        # Use with caution, this will drop all tables.
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
