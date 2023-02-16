import logging

from aiogram import Dispatcher

from data.config import ADMIN_ID


async def on_startup_notify(db: Dispatcher):
    for admin in ADMIN_ID:
        try:
            await db.bot.send_message(chat_id=admin, text="Бот запущен Admin")
        except Exception as err:
            logging.exception(err)
