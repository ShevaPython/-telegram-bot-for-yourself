from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_menu() -> ReplyKeyboardMarkup:
    """Создаем  клавитуру главного меню"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Мой аккаунт👤'),
            KeyboardButton(text='Музыка🎧'),
            KeyboardButton(text="Кошелек👛"),
            KeyboardButton(text='Погода⛅️')
        ],
        [
            KeyboardButton(text='Спрятать клавиатуру👀')
        ]
    ])
    return kb
