import asyncio
from commands_all import UserCommand
from utils.db_api.commands_database import test_connect_database, create_tables
from data_base import get_async_session


async def test_db():
    await test_connect_database()
    await create_tables()
    session =  get_async_session()
    user_command = UserCommand(session)
    # Создание пользователя
    # await user_command.create_user(user_id=1, name='Victoria', age=20, photo='awd', status='register')
    # await user_command.update_user(user_id=1,name='Виктория',photo='photo')
    balance =await user_command.get_user_balance(1)
    print(F'balance{balance}')
    await session.commit()
    await session.close()



if __name__ == "__main__":
    asyncio.run(test_db())
