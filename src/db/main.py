from sqlmodel import create_engine,text,SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine,async_sessionmaker 
from sqlalchemy.orm import sessionmaker
from src.config import Config
from src.books.models import Book

engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session