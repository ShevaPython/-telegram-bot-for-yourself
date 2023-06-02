import logging
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp, bot, types
from states.register_state import UpdateUserWallet
from utils.db_api import get_async_session
from utils.db_api.commands_all import UserCommand, WalletCommands, TransactionCommands
from keyboards.default import kb_wallet, kb_menu, kb_stop_fsm_all

logger = logging.getLogger(__name__)


@dp.message_handler(Text(equals='Кошелек👛'))
async def wallet_button(message: types.Message):
    """Кнопка кошелек"""
    '''Показать баланс пользователя'''
    try:
        async with get_async_session() as session:
            user_command = UserCommand(session)
            user = await user_command.get_user(message.from_user.id)
            if user:
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo='https://cdn.pixabay.com/photo/2017/06/29/20/04/wallet-2456004_640.jpg',
                                     caption=F"Добро пожаловать,я твой личный кошелек 🙋‍♂️",
                                     reply_markup=kb_wallet()
                                     )
                await bot.delete_message(chat_id=message.from_user.id,
                                         message_id=message.message_id)
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Пройдите регестрацию")
    except Exception as e:
        print(F"Произошла ошибка :{e}")


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

                await bot.send_photo(chat_id=message.from_user.id,
                                     photo='https://www.google.com/imgres?imgurl=http%3A%2F%2Fwebdiz.com.ua%2Fwp-content'
                                           '%2Fuploads%2F2021%2F04%2Fkak-zarabotat-mnogo-deneg.jpg&tbnid=UVXMbdrLkrHUQM&'
                                           'vet=12ahUKEwia-squuaT_AhURsioKHZugAJAQMyg9egQIARBa..i&imgrefurl=http%3A%2F%2'
                                           'Fwebdiz.com.ua%2Fkak-zarabotat-mnogo-deneg-bez-vlozhenii-po-kiosaki%2F&docid='
                                           'nQKLwc0v12wNgM&w=1200&h=908&q=%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%B'
                                           'D%D0%BE%D0%B5%20%D1%84%D0%BE%D1%82%D0%BE%20%D0%B4%D0%B5%D0%BD%D0%B5%D0%B3&ved'
                                           '=2ahUKEwia-squuaT_AhURsioKHZugAJAQMyg9egQIARBa',
                                     caption=f"Баланс пользователя: {balance} грн 💵.",
                                     reply_markup=kb_wallet())

                # Удаляем сообщение "Баланс💰"
                await bot.delete_message(chat_id=message.from_user.id,
                                         message_id=message.message_id)
            await session.commit()

    except Exception as e:
        logger.exception("Ошибка при выборке пользователя")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при выполнении запроса. Пожалуйста, попробуйте позже.")


@dp.message_handler(Text(equals='Пополнить баланс💵'), state=None)
async def update_balance_state(message: types.Message):
    '''Пополнить баланс'''
    try:
        async with get_async_session() as session:
            user_command = UserCommand(session)
            user = await user_command.get_user(message.from_user.id)

            if user is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.")
            else:
                await UpdateUserWallet.money.set()
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Введите сумму пополнения баланса:",
                                       reply_markup=kb_stop_fsm_all())
            await bot.delete_message(chat_id=message.from_user.id,
                                     message_id=message.message_id)

            await session.commit()

    except Exception as e:
        logger.exception("Ошибка при выборке пользователя")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при выполнении запроса. Пожалуйста, попробуйте позже.")


@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) <= 0,
                    state=UpdateUserWallet.money)
async def check_update_money(message: types.Message):
    """Проверка на валидность ввода"""
    return await message.reply(text=F"Сума пополнения должна быть числом \n"
                                    F"И не должна быть меньше 0",
                               reply_markup=kb_stop_fsm_all())


@dp.message_handler(state=UpdateUserWallet.money)
async def load_chain_money(message: types.Message, state: FSMContext):
    """Сохранения изменения в базу данных"""
    try:
        async with state.proxy() as data:
            data['money'] = float(message.text)
            change_balance = data['money']

        async with get_async_session() as session:
            wallet = WalletCommands(session)
            user_change_balance = await wallet.add_money_balance(owner_id=message.from_user.id,
                                                                 amount=change_balance)
            wallet_id = await wallet.get_wallet_from_user(owner_id=message.from_user.id)
            # Create a transaction
            transaction = await wallet.create_transaction(wallet_id=wallet_id.id, amount=change_balance)

            await bot.send_message(chat_id=message.from_user.id,
                                   text=F"Вашь баланс изменен на {change_balance} грн.✅\n"
                                        F"Cостовляет  грн {user_change_balance} 💵",
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

            wallet = await wallet_commands.get_wallet_from_user(owner_id=message.from_user.id)
            if wallet is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="У вас нет активного кошелька. Пожалуйста, создайте кошелек.")
                return

            await bot.send_message(chat_id=message.from_user.id,
                                   text="Введите месяц в формате 'ММ.ГГГГ' (например, 01.2023):",
                                   reply_markup=kb_stop_fsm_all())
            await UpdateUserWallet.month.set()

    except Exception as e:
        logger.exception("Ошибка при получении баланса за месяц")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при получении баланса за месяц. Пожалуйста, попробуйте позже.")


@dp.message_handler(lambda message: not re.match(r"\d{2}.\d{4}", message.text), state=UpdateUserWallet.month)
async def check_month_format(message: types.Message):
    """Проверка формата ввода месяца"""
    return await message.reply(text="Неверный формат месяца. Введите месяц в формате 'ММ.ГГГГ' (например, 01.2023):",
                               reply_markup=kb_stop_fsm_all())


@dp.message_handler(state=UpdateUserWallet.month)
async def show_month_balance(message: types.Message, state: FSMContext):
    """Отображение баланса за указанный месяц"""
    try:
        async with state.proxy() as data:
            month = message.text

        async with get_async_session() as session:
            wallet_commands = WalletCommands(session)
            transaction_commands = TransactionCommands(session)

            wallet = await wallet_commands.get_wallet_from_user(owner_id=message.from_user.id)
            if wallet is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="У вас нет активного кошелька. Пожалуйста, создайте кошелек.",
                                       reply_markup=kb_wallet())
                return

            transactions = await transaction_commands.get_transactions_by_month(wallet.id, month)
            total_balance = sum(transaction.amount for transaction in transactions)

            await bot.send_photo(chat_id=message.from_user.id,
                                 photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg2.freepng.ru%2F20180407%2'
                                       'Fdze%2Fkisspng-money-bag-clip-art-mony-5ac87e8be1bd13.1533603415230890359246.jpg'
                                       '&tbnid=MA2UCcT0Xi4_3M&vet=12ahUKEwia-squuaT_AhURsioKHZugAJAQMyhMegQIARB-..i&imgr'
                                       'efurl=https%3A%2F%2Fwww.freepng.ru%2Fpng-uo1dqr%2F&docid=xOzWg6rxCguzlM&w=900&h='
                                       '1040&q=%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%D0%B5%20%D1%84%D0%'
                                       'BE%D1%82%D0%BE%20%D0%B4%D0%B5%D0%BD%D0%B5%D0%B3&ved=2ahUKEwia-squuaT_AhURsioKHZu'
                                       'gAJAQMyhMegQIARB-',
                                 caption=f"Баланс за месяц {month} составляет: {total_balance} грн 💵",
                                 reply_markup=kb_wallet())

            await state.finish()

    except Exception as e:
        logger.exception(F"Ошибка при получении баланса за месяц :{e}")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при получении баланса за месяц. Пожалуйста, попробуйте позже.")


# # _____________________________________________________________________

@dp.message_handler(Text(equals='Взять с колшелька💵'))
async def take_of_balance_state(message: types.Message):
    '''Отнять баланс'''
    try:
        async with get_async_session() as session:
            user_command = UserCommand(session)
            user = await user_command.get_user(message.from_user.id)

            if user is None:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.")
            else:
                await UpdateUserWallet.take_money.set()
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Введите сумму взятия с баланса:",
                                       reply_markup=kb_stop_fsm_all())
            await bot.delete_message(chat_id=message.from_user.id,
                                     message_id=message.message_id)

            await session.commit()

    except Exception as e:
        logger.exception("Ошибка при выборке пользователя")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при выполнении запроса. Пожалуйста, попробуйте позже.")


@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) <= 0,
                    state=UpdateUserWallet.take_money)
async def check_take_of_update_money(message: types.Message):
    """Проверка на валидность ввода"""
    return await message.reply(text=F"Сума пополнения должна быть числом \n"
                                    F"И не должна быть меньше 0",
                               reply_markup=kb_stop_fsm_all())


@dp.message_handler(state=UpdateUserWallet.take_money)
async def load_take_off_money(message: types.Message, state: FSMContext):
    """Снятие средств с баланса"""
    try:
        change_balance = float(message.text)  # Отрицательная сумма для снятия с баланса

        async with get_async_session() as session:
            wallet = WalletCommands(session)
            wallet_owner = await wallet.get_wallet_from_user(owner_id=message.from_user.id)
            current_balance_owner = wallet_owner.balance

            if change_balance > current_balance_owner:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Вашь баланс на кошельке не можеть быть отрицательным 🤬",
                                       reply_markup=kb_wallet())
                return

            user_change_balance = await wallet.take_off_balance(owner_id=message.from_user.id, amount=change_balance)
            # Create a transaction
            transaction = await wallet.create_transaction(wallet_id=wallet_owner.id, amount=-change_balance)

            await session.commit()

        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Сумма {abs(change_balance)}💵 грн успешно снята с вашего баланса. \n"
                                    f"Текущий баланс составляет {user_change_balance}💵 грн.",
                               reply_markup=kb_wallet())
        await state.finish()
    except Exception as e:
        logger.exception("Ошибка при снятии средств с баланса")
        await bot.send_message(chat_id=message.from_user.id,
                               text="Произошла ошибка при снятии средств с баланса. Пожалуйста, попробуйте позже.")
