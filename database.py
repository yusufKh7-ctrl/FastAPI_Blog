from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
AsyncSessionlocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Base class for models | used for creating tables and for type hinting in models.py
class Base(DeclarativeBase):
    pass


# Dependency for getting a database session in routes
async def get_db():
    async with AsyncSessionlocal() as session:
        yield session
