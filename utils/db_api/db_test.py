import asyncio
from data_base import get_session
from models import Base


async def test_db():
    async with get_session() as session:
        async with session.begin():
            await session.run_sync(Base.metadata.drop_all)

        async with session.begin():
            await session.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_db())

