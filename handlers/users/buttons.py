from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text



@dp.message_handler(Text(equals='Музыка🎧'))
async def music_button(message: types.Message):
    """Кнопка музыка"""
    await message.answer(text=F"Слушаем музыку")


