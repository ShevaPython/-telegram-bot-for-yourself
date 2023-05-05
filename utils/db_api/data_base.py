import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from utils.db_api.models import Base
from data import config



async_engine = create_async_engine(config.POSTGRES_URI, echo=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession,
                             autocommit=False, autoflush=False)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



async def main():
    async with async_session() as session:
        async with session.begin():
            # выполнение асинхронных запросов
            pass


async def on_startup():
    await drop_tables()
    await create_tables()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete( drop_tables() )
    loop.run_until_complete(create_tables())
    loop.run_until_complete(main())
