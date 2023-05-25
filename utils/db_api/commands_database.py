from sqlalchemy import select

from .data_base import async_engine, async_session,get_async_session
from .models import Base


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync( Base.metadata.create_all )


async def drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync( Base.metadata.drop_all )



async def test_connect_database():
    try:
        async with get_async_session() as session:
            result = await session.execute(select(1))
            print( F" Подключения к базе даных результат : {result.scalar()}" )
    except Exception as e:
        print( F"Ошибка подключения к базе данных: {e}" )


