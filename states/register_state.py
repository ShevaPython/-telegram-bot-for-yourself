from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegister(StatesGroup):
    """FSM registration"""
    name = State()
    age = State()
    photo = State()

class UpdateUserWallet(StatesGroup):
    """Обновления кошелька пользователя"""
    money = State()
    month=State()


class UpdateUserData(StatesGroup):
    """Обновления данных пользователя"""
    name = State()
    age = State()
    photo = State()