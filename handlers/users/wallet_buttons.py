import logging
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot, types
from states.register_state import UpdateUserWallet
from utils.db_api import get_async_session
from utils.db_api.commands_all import UserCommand, WalletCommands, TransactionCommands
from keyboards.default import kb_wallet

logger = logging.getLogger(__name__)


@dp.message_handler(Text(equals='Баланс💰'))
async def show_balance(message: types.Message):
    '''Показать баланс пользователя'''
    try:
        async with get_async_session() as session:
            user_command = UserCommand(session)
            user = await user_command.get_user(message.from_user.id)

            if user is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.")
            else:
                balance = await user_command.get_user_balance(message.from_user.id)

                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Баланс пользователя: {balance} грн 💵.",
                                       reply_markup=kb_wallet())

                # Удаляем сообщение "Баланс💰"
                await bot.delete_message(chat_id=message.from_user.id,
                                         message_id=message.message_id)
            await session.commit()

    except Exception as e:
        logger.exception("Ошибка при выборке пользователя")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при выполнении запроса. Пожалуйста, попробуйте позже.")


@dp.message_handler(Text(equals='Пополнить баланс💵'))
async def show_balance(message: types.Message):
    '''Показать баланс пользователя'''
    try:
        async with get_async_session() as session:
            user_command = UserCommand(session)
            user = await user_command.get_user(message.from_user.id)

            if user is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.",
                                       reply_markup=kb_wallet())
            else:
                await UpdateUserWallet.money.set()
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Введите сумму пополнения баланса:",
                                       reply_markup=kb_wallet())
            await bot.delete_message(chat_id=message.from_user.id,
                                     message_id=message.message_id)

            await session.commit()

    except Exception as e:
        logger.exception("Ошибка при выборке пользователя")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при выполнении запроса. Пожалуйста, попробуйте позже.")


@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text)<=0,
                    state=UpdateUserWallet.money)
async def check_update_money(message: types.Message):
    """Проверка на валидность ввода"""
    await message.reply(text=F"Сума пополнения должна быть числом \n"
                             F"И не должна быть меньше 0",
                        reply_markup=kb_wallet())


@dp.message_handler(state=UpdateUserWallet.money)
async def load_chain_money(message: types.Message, state: FSMContext):
    """Сохранения изменения в базу данных"""
    try:
        async with state.proxy() as data:
            data['money'] = float(message.text)
            change_balance = data['money']

        async with get_async_session() as session:
            wallet = WalletCommands(session)
            user_change_balance = await wallet.update_wallet_balance(owner_id=message.from_user.id,
                                                                     amount=change_balance)
            wallet_id = await wallet.get_wallet(owner_id=message.from_user.id)
            # Create a transaction
            transaction=await wallet.create_transaction(wallet_id=wallet_id.id, amount=change_balance)


            await bot.send_message(chat_id=message.from_user.id,
                                    text=F"Вашь баланс изменен на {change_balance} грн.✅\n"
                                         F"Cостовляет  грн {user_change_balance}💵"
                                         F"Транзакция {transaction.amount}",
                                   reply_markup=kb_wallet())
            await session.commit()
            await state.finish()
    except Exception as e:
        logger.exception("Ошибка при пополнении баланса")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при пополнении баланса. Пожалуйста, попробуйте позже.")



@dp.message_handler(Text(equals='Баланс за определеный месяц 🌙'))
async def month_balance(message: types.Message):
    try:
        async with get_async_session() as session:
            wallet_commands = WalletCommands(session)

            wallet = await wallet_commands.get_wallet(owner_id=message.from_user.id)
            if wallet is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="У вас нет активного кошелька. Пожалуйста, создайте кошелек.",
                                       reply_markup=kb_wallet())
                return

            await bot.send_message(chat_id=message.from_user.id,
                                   text="Введите месяц в формате 'ММ.ГГГГ' (например, 01.2023):")
            await UpdateUserWallet.month.set()

    except Exception as e:
        logger.exception("Ошибка при получении баланса за месяц")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при получении баланса за месяц. Пожалуйста, попробуйте позже.")


@dp.message_handler(lambda message: not re.match(r"\d{2}.\d{4}", message.text), state=UpdateUserWallet.month)
async def check_month_format(message: types.Message):
    """Проверка формата ввода месяца"""
    await message.reply(text="Неверный формат месяца. Введите месяц в формате 'ММ.ГГГГ' (например, 01.2023):")


@dp.message_handler(state=UpdateUserWallet.month)
async def show_month_balance(message: types.Message, state: FSMContext):
    """Отображение баланса за указанный месяц"""
    try:
        async with state.proxy() as data:
            month = message.text

        async with get_async_session() as session:
            wallet_commands = WalletCommands(session)
            transaction_commands = TransactionCommands(session)

            wallet = await wallet_commands.get_wallet(owner_id=message.from_user.id)
            if wallet is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="У вас нет активного кошелька. Пожалуйста, создайте кошелек.",
                                       reply_markup=kb_wallet())
                return

            transactions = await transaction_commands.get_transactions_by_month(wallet.id, month)
            total_balance = sum(transaction.amount for transaction in transactions)

            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Баланс за месяц {month} составляет: {total_balance} грн 💵")

            await state.finish()

    except Exception as e:
        logger.exception(F"Ошибка при получении баланса за месяц :{e}")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при получении баланса за месяц. Пожалуйста, попробуйте позже.")
