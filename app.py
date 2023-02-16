async def on_startup(db):
    import filters
    filters.setup(db)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(db)

    from utils.set_botcommands import set_default_commands
    await set_default_commands(db)
    print("бот запущен")


if __name__ == "__main__":
    from aiogram import executor
    from handlers import db

    executor.start_polling(db, on_startup=on_startup, skip_updates=True)
