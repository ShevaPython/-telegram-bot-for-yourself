import os

import aiofiles
from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.dispatcher.filters import Text
from keyboards.default import kb_account, kb_stop_fsm_all
from loader import types, bot
from utils.db_api.commands_all import UserCommand
from utils.db_api.data_base import get_async_session
from states import UpdateUserData


@dp.message_handler(Text(equals='Мой аккаунт👤'))
async def account_button(message: types.Message):
    """Кнопка Мой Акаунт"""
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo='https://img.freepik.com/free-photo/workplace-late-at-night-night-work-concept'
                                           '_169016-17457.jpg?w=1380&t=st=1685721183~exp=1685721783~hmac=0ee03b9cb06f3564'
                                           'fb568947e856943410f11f142933e7a1c954bcb5a38cd110',
                                     caption=F"Привет,ты в своем личном кабинете 🙋‍♂️ \n"
                                             F"Здесь ты можешь изменить свои данные📂",
                                     reply_markup=kb_account())
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

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
                                       text='Ведите возраст : ',
                                       reply_markup=kb_stop_fsm_all())
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
    return await message.reply(text=F"Возраст должен состоять только из цыфр!И быть реальным",
                               reply_markup=kb_stop_fsm_all())


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
                                       text='Ведите имя : ',
                                       reply_markup=kb_stop_fsm_all())
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
    return await message.reply(text=F"Имя должно состоять только из букв!",
                               reply_markup=kb_stop_fsm_all())


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
                                       text='Отправте фотографию для изменения фото : ➡️➡️➡️ ',
                                       reply_markup=kb_stop_fsm_all())
                await UpdateUserData.photo.set()
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Пройдите регестрацию.")

    except Exception as e:
        print(f"Ошибка при выборке пользователя: {e}")
        pass


@dp.message_handler(lambda message: not message.photo, state=UpdateUserData.photo)
async def check_photo(message: types.Message):
    """Проверка на фотографию"""
    return await message.reply(text=F"Это не фото,не обманывай!🙁",
                               reply_markup=kb_stop_fsm_all())


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
