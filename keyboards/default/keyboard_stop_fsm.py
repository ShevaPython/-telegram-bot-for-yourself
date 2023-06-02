from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_stop_fsm_register() -> ReplyKeyboardMarkup:
    """Клавиатура отмены состояния"""
    button_cancel = KeyboardButton("Отмена регистрации🔙️")
    keyboard_stop_fsm = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
    return keyboard_stop_fsm

def kb_stop_fsm_all() -> ReplyKeyboardMarkup:
    """Клавиатура отмены состояния главное меню"""
    button_cancel = KeyboardButton("Отмена операции◀️")
    keyboard_stop_fsm = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
    return keyboard_stop_fsm



def kb_stop_fsm_weather() -> ReplyKeyboardMarkup:
    """Клавиатура отмены состояния главное меню"""
    button_cancel = KeyboardButton("Отмена операции ⛅️")
    keyboard_stop_fsm = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)
    return keyboard_stop_fsm