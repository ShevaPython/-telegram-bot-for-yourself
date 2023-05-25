from aiogram.dispatcher.filters import Text
from loader import dp, bot, types
from utils.db_api import get_async_session, User, Wallet
from utils.db_api.commands_user import UserCommand
from sqlalchemy import select


# @dp.message_handler(Text(equals='Баланс💰'))
# async def show_balance(message: types.Message):
#     '''Показать баланс пользователя'''
#     try:
#         async with get_async_session() as session:
#             user = await session.get(User, message.from_user.id)
#
#             if user is None:
#                 await bot.send_message(chat_id=message.from_user.id,
#                                        text="Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.")
#             else:
#                 wallet = await session.execute(select(Wallet).where(Wallet.owner_id == user.user_id))
#                 wallet_ = wallet.scalar_one()
#
#                 await bot.send_message(chat_id=message.from_user.id,
#                                        text=f"Баланс пользователя: {wallet_.balance}")
#
#             await session.commit()
#
#     except Exception as e:
#         print(f"Ошибка при выборке пользователя: {e}")
@dp.message_handler(Text(equals='Баланс💰'))
async def show_balance(message: types.Message):
    '''Показать баланс пользователя'''
    try:
        async with await get_async_session() as session:
            user = await session.get(User, message.from_user.id)

            if user is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.")
            else:
                wallet = await session.execute(select(Wallet).where(Wallet.owner_id == user.user_id))
                wallet_ = wallet.scalar_one()

                balance = wallet_.balance if wallet_ else 0
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Баланс пользователя: {balance}")

    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")

