from aiogram.dispatcher.filters import Text
from aiogram import types

from keyboards.default import kb_menu

from loader import dp,bot


@dp.message_handler(Text(equals="Главное меню▶️"))
async def command_menu(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Добро пожаловать в Главное меню▶️",
                           reply_markup=kb_menu())

