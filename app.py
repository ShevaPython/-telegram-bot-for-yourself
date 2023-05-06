import filters
import middlewares
from utils.notify_admins import on_startup_notify
from utils.set_botcommands import set_default_commands
from utils.db_api import create_tables,test_connect_database,drop_tables


async def on_startup(dp):
    filters.setup( dp )

    middlewares.setup( dp )

    await on_startup_notify( dp )


    await set_default_commands( dp )
    print( "бот запущен" )

    await test_connect_database()

    print('Удаления таблиц')
    await drop_tables()

    print( "Создание таблиц" )
    await create_tables()





if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling( dp, on_startup=on_startup, skip_updates=True)
