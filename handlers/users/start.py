from aiogram import types
from loader import db, bot
from filters import IsPrivate


@db.message_handler(IsPrivate(),text='/start')
async def command_start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=F"Привет {message.from_user.full_name}👋!\n"
                                                              F"Для работы с ботом пройди регестрацию здесь -> /register🖥"
                           )
