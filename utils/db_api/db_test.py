import asyncio
from models import Base
from loader import async_engine
from commands_user import delete_user,create_user,update_user,get_user
from commands_database import init_database,test_connect_database


async def test_db():
    await test_connect_database()
    await init_database()
    await create_user(1,'Сергей',30,'dasdasd')
    await create_user(2, 'Виктория', 28, 'фывфывфыв' )
    await get_user(1)
    await get_user(2)


if __name__ == "__main__":
    asyncio.run(test_db())

