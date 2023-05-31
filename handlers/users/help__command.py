from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, callback_query


from utils.db_api.commands_all import UserCommand
from utils.db_api.data_base import get_async_session
from loader import dp, bot

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_account = InlineKeyboardButton('Мой аккаунт', callback_data='my_account')
    button_info = InlineKeyboardButton('Информация', callback_data='info')
    button_settings = InlineKeyboardButton('Настройки', callback_data='settings')
    button_help = InlineKeyboardButton('Помощь', callback_data='help')
    keyboard.add(button_account, button_info, button_settings, button_help)
    return keyboard


def kb_account():
    keyboard = InlineKeyboardMarkup()
    button_back = InlineKeyboardButton('Главное меню', callback_data='main_menu')
    keyboard.add(button_back)
    return keyboard

@dp.message_handler(Command('help'))
async def start(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=kb_main_menu())


@dp.callback_query_handler(text='my_account')
async def account_button(callback_query: CallbackQuery):
    try:
        user_id = callback_query.from_user.id

        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(user_id)

            if user:
                await bot.send_message(chat_id=user_id,
                                       text="Привет, ты в своем личном кабинете 🙋‍♂️",
                                       reply_markup=kb_account())
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
                await bot.send_sticker(chat_id=user_id,
                                       sticker='CAACAgIAAxkBAAEHh7Fj2Sf4gLEBGA7xgulqRXnzsCXGPwACCwMAAm2wQgN_tBzazKZEJS0E')
            else:
                await bot.send_message(chat_id=user_id,
                                       text="Пройдите регистрацию.")
    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass


@dp.callback_query_handler(text='main_menu')
async def main_menu_button(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Вы вернулись в главное меню.",
                           reply_markup=kb_main_menu())




