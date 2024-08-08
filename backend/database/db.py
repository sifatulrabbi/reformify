import logging
from typing import Annotated, AsyncContextManager
from fastapi import Depends
from contextlib import asynccontextmanager
from configs import DB_HOST, DB_NAME, DB_PASS, DB_USER
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_async_engine(url)
metadata = MetaData()


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_db_session():
    # async with engine.begin() as session:
    SessionMaker = async_sessionmaker(bind=engine)
    async with SessionMaker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            raise err
        finally:
            await session.close()


DBConn = AsyncContextManager[AsyncSession]
InjectDB = Annotated[DBConn, Depends(get_db_session)]


async def migration():
    logging.info("Starting the migration")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Done migrating")
