from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from data import config

async_engine = create_async_engine(config.POSTGRES_URI, echo=True)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession,
                             autocommit=False, autoflush=False)


# def get_async_session() -> AsyncSession:
#     return async_session()

async def get_async_session() -> AsyncSession:
    async with async_engine.begin() as connection:
        session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
        async with session() as async_session:
            return async_session
