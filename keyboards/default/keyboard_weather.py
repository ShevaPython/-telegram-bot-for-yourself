from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_weather() -> ReplyKeyboardMarkup:
    """Создаем  клавитуру кошелька """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='На сегодня ⛅️'),
            KeyboardButton(text='На 5 дней ⛅️'),

        ],
        [
            KeyboardButton(text='Главное меню▶️')
        ]
    ])
    return kb
