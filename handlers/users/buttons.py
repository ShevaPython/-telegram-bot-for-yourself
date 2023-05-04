import keyboards.default
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import kb_wallet

"""Кнопки главного меню"""


@dp.message_handler(Text(equals='Спрятать клавиатуру👀'))
async def hide_kb_menu_button(message: types.Message):
    """Убрать клавиатуру"""
    await message.answer(text=F"Готово ✅ \n"
                              F"Для повторного вызова клавиатуры введи->  Главное меню▶️",
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='Мой аккаунт👤'))
async def joke_button(message: types.Message):
    """Кнопка Анекдоты"""
    await message.answer(text=F"Профиль пользователя")


@dp.message_handler(Text(equals='Музыка🎧'))
async def music_button(message: types.Message):
    """Кнопка музыка"""
    await message.answer(text=F"Слушаем музыку")


@dp.message_handler(Text(equals='Кошелек👛'))
async def wallet_button(message: types.Message):
    """Кнопка кошелек"""
    await message.answer(text=F"Мой баланс",
                         reply_markup=keyboards.default.kb_wallet()
                         )


@dp.message_handler(Text(equals='Погода⛅️'))
async def weather_button(message: types.Message):
    """Кнопка погоды"""
    await message.answer(text=F"Прогноз погоды")
