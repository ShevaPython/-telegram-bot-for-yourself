from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_account() -> ReplyKeyboardMarkup:
    """Создаем  клавитуру акаунта"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Мои данные💻'),
            KeyboardButton(text='Главное меню▶️')


        ],
        [
            KeyboardButton(text='Изменить фото👤'),
            KeyboardButton(text="Изменить имя🫵"),
            KeyboardButton(text='Изменить возраст🫀'),
        ]
    ])
    return kb