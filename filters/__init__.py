from aiogram import Dispatcher
from .private_chat import IsPrivate

def setup(db:Dispatcher):
    db.filters_factory.bind(IsPrivate)