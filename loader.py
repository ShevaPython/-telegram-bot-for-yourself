from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.data_base import async_session

from data import config

# Создаем  переменную бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML,)
# Создаем хранилище
storage = MemoryStorage()
# Создаем деспетчер
dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'async_session']

