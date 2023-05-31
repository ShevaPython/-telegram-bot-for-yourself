from aiogram.dispatcher.filters import Text
from aiogram import types

from utils.db_api.commands_all import UserCommand
from utils.db_api.data_base import get_async_session

from keyboards.default import kb_menu

from loader import dp, bot


@dp.message_handler(Text(equals="Главное меню▶️"))
async def command_menu(message: types.Message):
    try:
        async with get_async_session()as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Добро пожаловать в Главное меню▶️",
                                       reply_markup=kb_menu())
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Пройдите регестрацию')
    except Exception as e:
        print(F"Произошла ошибка {e}")