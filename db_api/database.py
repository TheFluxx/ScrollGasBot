from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import asynccontextmanager
from data.config import DB_DRIVER, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME

Base = declarative_base()

engine = create_async_engine(
    f'{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}',
    future=True,
)


async def create_base():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def async_session_generator():
    return sessionmaker(
        engine, class_=AsyncSession
    )


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
