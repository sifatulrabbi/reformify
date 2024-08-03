import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from configs import DB_HOST, DB_NAME, DB_PASS, DB_USER

url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_async_engine(url, echo=True)


class Base(DeclarativeBase):
    pass


async def get_db_session():
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            raise err
        finally:
            await session.close()


async def migration():
    logging.info("Starting the migration")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Done migrating")
