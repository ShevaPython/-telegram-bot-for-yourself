from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_wallet() -> ReplyKeyboardMarkup:
    """Создаем  клавитуру кошелька """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Баланс💰'),
            KeyboardButton(text='Пополнить баланс💵'),
            KeyboardButton(text='Взять с колшелька💵')

        ],
        [
            KeyboardButton(text="Баланс за определеный месяц 🌙"),
            KeyboardButton(text='Главное меню▶️')
        ]
    ])
    return kb
