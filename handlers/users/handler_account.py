import os

import aiofiles
from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.dispatcher.filters import Text
from keyboards.default import kb_account
from loader import types, bot
from utils.db_api.commands_all import UserCommand
from utils.db_api.data_base import get_async_session
from states import UpdateUserData


# Мои данные💻
# Изменить возраст🫀
@dp.message_handler(Text(equals='Мой аккаунт👤'))
async def account_button(message: types.Message):
    """Кнопка Мой Акаунт"""
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_message(chat_id=message.from_user.id,
                                       text=F"Привет,ты в своем личном кабинете 🙋‍♂️",
                                       reply_markup=kb_account())
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
                await bot.send_sticker(chat_id=message.from_user.id,
                                       sticker='CAACAgIAAxkBAAEHh7Fj2Sf4gLEBGA7xgulqRXnzsCXGPwACCwMAAm2wQgN_tBzazKZEJS0E')
            else:
                await bot.send_message("Пройдите регестрацию.")
    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass


@dp.message_handler(Text(equals='Мои данные💻'))
async def show_account(message: types.Message):
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                caption = F"Имя пользователя : {user.name} ✅ \n" \
                          F"Возраст : {user.age} ✅ \n" \
                          F"Дата регистрации : {user.create_at.date()} ✅ \n" \
                          F"Дата обновления : {user.updated_at.date()} ✅"

                async with aiofiles.open(user.photo, 'rb') as photo_file:
                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo=photo_file,
                                         caption=caption,
                                         reply_markup=kb_account())
                    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
                    await bot.send_sticker(chat_id=message.from_user.id,
                                           sticker='CAACAgIAAxkBAAEJKkxkdzNCszWSuCJNlyAwToQ3KTk_NAACGwMAAm2wQgMfr3Hx-w4MSi8E')
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Пройдите регестрацию.")
            await session.commit()
            await session.close()
    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass


@dp.message_handler(Text(equals='Изменить возраст🫀'))
async def change_age(message: types.Message):
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Ведите возраст : ')
                await UpdateUserData.age.set()
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Пройдите регестрацию.")

    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 120 or float(message.text) < 5,
                    state=UpdateUserData.age)
async def check_update_age(message: types.Message):
    """Проверка на коректность ввода возраста"""
    await message.reply(text=F"Возраст должен состоять только из цыфр!И быть реальным")


@dp.message_handler(state=UpdateUserData.age)
async def load_update_age(message: types.Message, state: FSMContext):
    """Сохранения возраста в бд!"""
    async with state.proxy() as data:
        data["age"] = int(message.text)
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                user.age = data['age']
            await session.commit()
            await session.close()
        await bot.send_message(chat_id=message.from_user.id,
                               text=F"Мы изменили вознаст на {user.age}",
                               reply_markup=kb_account())
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker='CAACAgIAAxkBAAEJKqFkd0uFiDAhpFSj1WKtYPA-OgVJ_wACZgADWbv8JZy8mJK_t4cXLwQ')
        await state.finish()
    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass

    await state.finish()


@dp.message_handler(Text(equals='Изменить имя🫵'))
async def change_name(message: types.Message):
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Ведите имя : ')
                await UpdateUserData.name.set()
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Пройдите регестрацию.")

    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass


@dp.message_handler(lambda message: not message.text.isalpha(),
                    state=UpdateUserData.name)
async def check_update_name(message: types.Message):
    """Проверка на коректность ввода имени"""
    await message.reply(text=F"Имя должно состоять только из букв!")


@dp.message_handler(state=UpdateUserData.name)
async def load_update_name(message: types.Message, state: FSMContext):
    """Сохранения возраста в бд!"""
    async with state.proxy() as data:
        data["name"] = str(message.text)
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                user.name = data['name']
                await session.commit()
                await session.close()
            else:
                pass
        await bot.send_message(chat_id=message.from_user.id,
                               text=F"Мы изменили имя на {user.name}",
                               reply_markup=kb_account())
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker='CAACAgIAAxkBAAEJKqFkd0uFiDAhpFSj1WKtYPA-OgVJ_wACZgADWbv8JZy8mJK_t4cXLwQ')

        await state.finish()
    except Exception as e:
        print(F"Ошибка {e} ")


@dp.message_handler(Text(equals='Изменить фото👤'))
async def change_update_photo(message: types.Message):
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Отправте фотографию для изменения фото : ➡️➡️➡️ ')
                await UpdateUserData.photo.set()
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Пройдите регестрацию.")

    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass


@dp.message_handler(lambda message: not message.photo, state=UpdateUserData.photo)
async def check_photo(message: types.Message):
    """Проверка на фотографию"""
    await message.reply(text=F"Это не фото,не обманывай!🙁")


@dp.message_handler(content_types=types.ContentType.PHOTO, state=UpdateUserData.photo)
async def load_update_photo(message: types.Message, state: FSMContext):
    try:
        # Получение идентификатора пользователя
        user_id = message.from_user.id

        # Создание папки с идентификатором пользователя, если она не существует
        user_folder = os.path.join("photos", str(user_id))

        # Проверка наличия директории
        if os.path.isdir(user_folder):
            # Удаление всех файлов внутри директории
            for file_name in os.listdir(user_folder):
                file_path = os.path.join(user_folder, file_name)
                os.remove(file_path)
        else:
            # Создание директории, если она не существует
            os.makedirs(user_folder, exist_ok=True)

        # Сохранение фотографии на диск
        photo_path = os.path.join(user_folder, "file.jpg")
        await message.photo[-1].download(destination=photo_path)

        # Продолжение обработки или сохранение пути к фотографии в состояние FSMContext

    except Exception:
        # Обработка ошибки, если загруженный файл не является изображением
        await message.reply("Ошибка! Пожалуйста, загрузите изображение.")
        return
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                user.photo = photo_path
            await session.commit()
            await session.close()
    except Exception as e:
        print(F"Ошибка {e}")
    # Отправка фотографии с помощью контекстного менеджера
    async with aiofiles.open(photo_path, 'rb') as photo_file:
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=photo_file,
            caption=F"Теперь фотография Вашего профиля выгоядет так 📸",
            reply_markup=kb_account()
        )

    await state.finish()
