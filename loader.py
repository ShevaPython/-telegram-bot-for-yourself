from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

# Создаем  переменную бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# Создаем хранилище
storage = MemoryStorage()
# Создаем деспетчер
db = Dispatcher(bot, storage=storage)
