from aiogram.dispatcher import FSMContext
import aiofiles
import os
from aiogram.dispatcher.filters import Command
from states import UserRegister
from keyboards.default import kb_menu
from loader import dp, bot, types
from utils.misc import rate_limit
from utils.db_api.commands_all import UserCommand
from utils.db_api.data_base import get_async_session


@rate_limit(limit=10, key="/register")
@dp.message_handler(Command("register"))
async def register(message: types.Message, state: FSMContext):
    """Начало регестрации пользователя"""

    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user is None:
                await bot.send_sticker(chat_id=message.from_user.id,
                                       sticker='CAACAgIAAxkBAAEJKhZkdyUeLsuissI6iQ9HOIZArcWOCgACHAADlp-MDpnUab5i8nnlLwQ')
                await bot.send_message(chat_id=message.from_user.id,
                                       text=F"Регестрация началась🚦 \n"
                                            F"Введите свое имя :")
                await UserRegister.name.set()
            elif user.status == 'register':
                await bot.send_message(chat_id=message.from_user.id,
                                       text=F'Привет {message.from_user.full_name} Ты уже зарегистрирован!')
                await bot.send_sticker(chat_id=message.from_user.id,
                                       sticker='CAACAgIAAxkBAAEJKh1kdyV4xqZSG_MG8d1R_jSrrpTI-QACfgADlp-MDnGDEZ4sXLblLwQ')


    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
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


@dp.message_handler(content_types=types.ContentType.PHOTO, state=UserRegister.photo)
async def load_photo(message: types.Message, state: FSMContext):
    try:
        # Получение идентификатора пользователя
        user_id = message.from_user.id

        # Создание папки с идентификатором пользователя, если она не существует
        user_folder = os.path.join("photos", str(user_id))
        os.makedirs(user_folder, exist_ok=True)

        # Сохранение фотографии на диск
        photo_path = os.path.join(user_folder, "file.jpg")
        await message.photo[-1].download(destination=photo_path)
    except Exception:
        # Обработка ошибки, если загруженный файл не является изображением
        await message.reply("Ошибка! Пожалуйста, загрузите изображение.")
        return

    async with state.proxy() as data:
        data['status'] = 'register'
    # Сохранение пути к фотографии в базу данных
    user_cmd = UserCommand(get_async_session())
    await user_cmd.create_user(
        user_id=message.from_user.id,
        name=data["name"],
        age=data["age"],
        photo=photo_path,
        status=data["status"],
    )

    # Отправка фотографии с помощью контекстного менеджера
    async with aiofiles.open(photo_path, 'rb') as photo_file:
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=photo_file,
            caption=F"Ваши данные сохранены. Спасибо за регистрацию! 🎯\n"
                    F"Имя: {data['name']}\n"
                    F"Ваш возраст: {data['age']}\n"
                    F"Вам доступно главное меню!\n",
            reply_markup=kb_menu()
        )

    await bot.send_message(
        chat_id=message.from_user.id,
        text=F"Теперь в вашем разделе присутствует кошелек!\n"
             F"На данный момент его баланс составляет {0.0}",
    )

    await state.finish()
