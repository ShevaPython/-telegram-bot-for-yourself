import asyncio

from data import config
from utils.db_api.db_gino import db
from utils.db_api import quick_commands as commands


async def db_test():
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    await commands.add_user(1)

    users = await commands.select_all_users()
    print(users)

    count = await commands.count_all_users()
    print(count)

    user = await commands.select_user(1)
    print(user)



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(db_test())
    except KeyboardInterrupt:
        pass
