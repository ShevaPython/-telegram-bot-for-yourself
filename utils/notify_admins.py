import logging

from aiogram import Dispatcher

from data.config import ADMIN_ID


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMIN_ID:
        try:
            await dp.bot.send_message(chat_id=admin, text=f"Бот запущен Admin")
            logging.basicConfig( level=logging.DEBUG)
        except Exception as err:
            logging.exception(err)
