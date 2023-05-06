from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from states import UserRegister
from keyboards.default import kb_menu
from loader import dp, bot, types
from utils.misc import rate_limit
from utils.db_api import commands_user as command


@rate_limit(limit=10, key="/register")
@dp.message_handler(Command("register"))
async def register(message: types.Message, state: FSMContext):
    """Начало регестрации пользователя"""

    try:

        user = await command.select_user( message.from_user.id )
        if user is None:
            await bot.send_message( chat_id=message.from_user.id,
                                    text=F"Регестрация началась🚦 \n"
                                         F"Введите свое имя :" )
            await command.add_user( user_id=message.from_user.id )
            await UserRegister.name.set()
        elif user.status == 'register':
            await bot.send_message( chat_id=message.from_user.id,
                                    text=F'Привет {message.from_user.full_name} Ты уже зарегистрирован!' )


    except Exception as e:
        print( f"Ошибка при выборке пользователя: {e}" )
        pass



@dp.message_handler(lambda message: not message.text.isalpha(),
                    state=UserRegister.name)
async def check_name(message: types.Message):
    """Проверка на коректность ввода имени"""
    await message.reply(text=F"Имя должно состоять только из букв!")


@dp.message_handler(state=UserRegister.name)
async def load_name(message: types.Message, state: FSMContext):
    """Сохранения имени в бд!"""
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text=F'Сколько тебе лет {data["name"]}??')

    await UserRegister.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 120 or float(message.text) < 5,
                    state=UserRegister.age)
async def check_age(message: types.Message):
    """Проверка на коректность ввода возраста"""
    await message.reply(text=F"Возраст должен состоять только из цыфр!И быть реальным")


@dp.message_handler(state=UserRegister.age)
async def load_age(message: types.Message, state: FSMContext):
    """Сохранения возраста в бд!"""
    async with state.proxy() as data:
        data["age"] = int(message.text)
    await bot.send_message(chat_id=message.from_user.id,
                           text=F'Отправь мне свою фотографию -> 📷')

    await UserRegister.next()


@dp.message_handler(lambda message: not message.photo, state=UserRegister.photo)
async def check_photo(message: types.Message):
    """Проверка на фотографию"""
    await message.reply(text=F"Это не фото,не обманывай!")


@dp.message_handler(content_types=['photo'], state=UserRegister.photo)
async def load_photo(message: types.Message, state: FSMContext):
    """Сохранения фото в бд"""
    async with state.proxy() as data:
        data["photo"] = str(message.photo[0].file_id)
        await UserRegister.next()
    async with state.proxy() as data:
        data['status'] = 'register'
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=data['photo'],
                         caption=F"Ваши данные сохранены.Спасибо,за регестрацию!🎯 \n"
                                 F"Имя: {data['name']}\n"
                                 F"Ваш возраст :{data['age']}\n"
                                 F"Теперь вам доступно главное меню!\n",
                         reply_markup=kb_menu())
    await command.update_user_data(user_id=message.from_user.id,state=state)
    await state.finish()


