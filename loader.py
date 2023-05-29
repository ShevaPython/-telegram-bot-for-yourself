from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
import os
# Создаем  переменную бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML,)
# Создаем хранилище
storage = MemoryStorage()
# Создаем деспетчер
dp = Dispatcher(bot, storage=storage)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__all__ = ['bot', 'storage', 'dp','BASE_DIR']

