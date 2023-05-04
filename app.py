async def on_startup(dp):
    import filters
    filters.setup(dp)
    import middlewares
    middlewares.setup(dp)

    from loader import db
    from utils.db_api.db_gino import on_startup
    print('Подключения к Postgresql')
    await on_startup(dp)

    print('Удаления базы данных')
    await db.gino.drop_all()

    print('Создания таблиц Postgresql')
    await db.gino.create_all()
    print('Готово')

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_botcommands import set_default_commands
    await set_default_commands(dp)
    print("бот запущен")


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
