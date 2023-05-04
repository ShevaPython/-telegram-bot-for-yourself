from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegister(StatesGroup):
    """FSM registration"""
    name = State()
    age = State()
    photo = State()

