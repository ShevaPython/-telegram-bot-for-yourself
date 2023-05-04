from aiogram import types
from loader import dp


@dp.message_handler(text='/help')
async def command_help(message: types.Message):
    await message.answer(F"Привет {message.from_user.full_name}!\n"
                         F"Список команд здесь!")
