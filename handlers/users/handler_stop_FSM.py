from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from loader import dp, bot, types
from keyboards.default import kb_menu,kb_weather


@dp.message_handler(Text(equals="Отмена регистрации🔙️"), state='*')
async def cancel_handler_fsm_register(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    # Очистка состояния машины
    await state.finish()

    # Отправка сообщения с главным меню и клавиатурой
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы отменили регестрацию, все предыдущие действия отменены.🤨",
                           reply_markup=ReplyKeyboardRemove()
                           )


@dp.message_handler(Text(equals="Отмена операции◀️"), state='*')
async def cancel_handler_fsm_stop_all(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    # Очистка состояния машины
    await state.finish()

    # Отправка сообщения с главным меню и клавиатурой
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы вернулись в главное меню, все предыдущие действия отменены.🤨",
                           reply_markup=kb_menu()
                           )


@dp.message_handler(Text(equals="Отмена операции ⛅️"), state='*')
async def cancel_handler_fsm_stop_weather(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    # Очистка состояния машины
    await state.finish()

    # Отправка сообщения с главным меню и клавиатурой
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы вернулись в меню погоды, все предыдущие действия отменены.🤨",
                           reply_markup=kb_weather()
                           )