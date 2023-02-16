from aiogram import types


async def set_default_commands(db):
    await db.bot.set_my_commands([
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('/register', 'Регестрация для начала работы с ботом')
    ])
