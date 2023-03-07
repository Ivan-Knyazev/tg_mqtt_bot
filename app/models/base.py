# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from typing import Any

from app.env import POSTGRES_URI
from app.models.models import Base

engine: Any = None
async_session: Any = None

# Base = declarative_base()
engine = engine or create_async_engine(POSTGRES_URI)

async_session = async_session or sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# async_session = async_session or async_sessionmaker(
#     bind=engine, expire_on_commit=False
# )

# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
