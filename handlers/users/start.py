from aiogram import types
from loader import dp, bot
from filters import IsPrivate
from utils.misc import rate_limit
from utils.db_api import commands_user
from keyboards.default import kb_menu


@rate_limit(limit=5, key="/start")
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    try:
        user = await commands_user.get_user(user_id=message.from_user.id)
        if user:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="<b>Добро пожаловать в Наш телеграм бот</b>👋!",
                                   reply_markup=kb_menu())
        else:
            await bot.send_message( chat_id=message.from_user.id,
                                    text=F"Вы ,{message.from_user.full_name}, еще не зарегестрировались!🙁\n"
                                         F"Для работы с ботом пройди регестрацию здесь -> /register🖥" )

    except Exception as e:
        print( f"Ошибка при выборке пользователя: {e}" )
        pass
