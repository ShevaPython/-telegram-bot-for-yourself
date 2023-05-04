from aiogram import types
from loader import dp, bot
from filters import IsPrivate
from utils.misc import rate_limit
from utils.db_api import quick_commands
from keyboards.default import kb_menu


@rate_limit(limit=5, key="/start")
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    try:
        user = await quick_commands.select_user(message.from_user.id)
        if user:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="<b>Добро пожаловать в Наш телеграм бот</b>👋!",
                                   reply_markup=kb_menu())
        else:
            await bot.send_message( chat_id=message.from_user.id,
                                    text=F"Привет {message.from_user.full_name}👋!\n"
                                         F"Для работы с ботом пройди регестрацию здесь -> /register🖥" )

    except Exception as e:
        print( f"Ошибка при выборке пользователя: {e}" )
        pass
