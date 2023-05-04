from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware


def setup(db: Dispatcher):
    db.middleware.setup(ThrottlingMiddleware())
