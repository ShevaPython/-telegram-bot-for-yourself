from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_stop_fsm() -> ReplyKeyboardMarkup:
    """Создаем  клавитуру главного меню"""
    button_cancel = KeyboardButton("Отмена операции🙅‍♂️")
    keyboard_stop_fsm = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
    return keyboard_stop_fsm


