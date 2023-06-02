import datetime
from pprint import pprint

import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default import kb_weather, kb_stop_fsm_weather
from loader import bot, types, dp
from utils.db_api.commands_all import UserCommand
from utils.db_api.data_base import get_async_session
from states import WeatherStateOneday, WeatherStatWeek
from data.config import APIWEATHER


@dp.message_handler(Text(equals='Погода⛅️'))
async def weather_button(message: types.Message):
    """Обработка кнопки погоды"""
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = await user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Fimage.winudf.com%2'
                                           'Fv2%2Fimage1%2FY29tLmluaXR5Lmdvb2R3ZWF0aGVyX3NjcmVlbl9ydS1SVV82XzE1NTgwNjM2NDNfMDIz%2Fscreen-6.jpg%3Ffakeurl%3D1%26type%3D.jpg&'
                                           'tbnid=eEFP2fLvnUJZNM&vet=10CDoQMyiBAWoXChMIqI_mm-uh_wIVAAAAAB0AAAAAEAI..i&imgrefurl=https%3A%2F%2Fapkpure.com%2Fru%2'
                                           'Fgood-morning-weather-free-world-weather-forecast%'
                                           '2Fcom.inity.goodweather&docid=dfqFRTWOgb5FjM&w=1100&h=814&'
                                           'itg=1&q=%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%D0%B5%20%D1%84%D0%BE%D1%82%D0%BE%20%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B&'
                                           'ved=0CDoQMyiBAWoXChMIqI_mm-uh_wIVAAAAAB0AAAAAEAI',
                                     caption='Смотри погоду на сегодня!✅  Или на 5 дней 👁',
                                     reply_markup=kb_weather()
                                     )
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Пройдите регистрацию .")

    except Exception as e:
        print(F'Ошибка при выборе пользователя {e}')


@dp.message_handler(Text(equals='На сегодня ⛅️'), state=None)
async def weather_now(message: types.Message):
    """Прогнос погоды на сегодня"""
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Введите город  или страну 🌍',
                                       reply_markup=kb_stop_fsm_weather())
                await WeatherStateOneday.city.set()

            else:
                await bot.send_message(chat_id=message.from_user.id, text=F"Пройдите регестрацию")
    except Exception as e:
        print(F"Ошибка при выборке пользователя")


@dp.message_handler(state=WeatherStateOneday.city)
async def check_correct_data_city(message: types.Message, state: FSMContext):
    city = message.text
    try:

        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        r = requests.get(
            F"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIWEATHER}&units=metric&lang=ua,uk"
        )

        data = r.json()

        city_name = data['name']
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        temp = data['main']['temp']
        country = data['sys']['country']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        speed_wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset - sunrise

        # Формирование сообщения с результатами погоды
        weather_message = (
            F'<em>Погода в городе: {city_name}</em>\n'
            F'<b>Температура сейчас: {temp}°C {wd} </b>\n'
            F'<em>***Текущая дата: {datetime.datetime.now().date()}***</em>\n'
            F'<em>Страна: {country}\n</em>'
            F'<em>Влажность: {humidity}%\n</em>'
            F'<em>Давление: {pressure} мм.рт.ст.\n</em>'
            F'<em>Скорость ветра: {speed_wind} м/с\n</em>'
            F'<em>Рассвет: {sunrise}\n</em>'
            F'<em>Закат: {sunset}</em> \n'
            F'<em>Продолжительность дня: {length_of_the_day}</em>'
        )

        await bot.send_photo(chat_id=message.from_user.id,
                             caption=weather_message,
                             photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Fotkrytkivsem.ru%2Fwp-content%2Fup'
                                   'loads%2F2021%2F03%2Fkartinka-dobrogo-dnya-i-horoshey-pogody.jpg&tbnid=fjxjmEGe36aCnM'
                                   '&vet=12ahUKEwiAw9G0-qH_AhUGpIsKHSniBLsQMyhFegQIARBt..i&imgrefurl=https%3A%2F%2Fotkryt'
                                   'kivsem.ru%2Fdlya-horoshego-nastroeniya%2Fdnevnye%2Fkartinka-dobrogo-dnya-i-horoshey-'
                                   'pogody%2F&docid=IWF1MG3_hiK-jM&w=600&h=600&q=%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0'
                                   '%BA%D0%B0%20%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0'
                                   '%B0%D1%82%D0%BD%D0%BE&ved=2ahUKEwiAw9G0-qH_AhUGpIsKHSniBLsQMyhFegQIARBt',
                             reply_markup=kb_weather())
        await state.finish()

    except Exception as e:
        print(F"Ошибка при получении погоды: {e}")
        await message.answer(text=F"Такого города или страны не существует ☝️"
                                  F"Проверте корректность даных и попробуйте снова🙄",
                             reply_markup=kb_stop_fsm_weather())


# На неделю ⛅️
@dp.message_handler(Text(equals='На 5 дней ⛅️'),state=None)
async def show_weather_week(message: types.Message):
    """Прогнос погоды на неделю"""
    try:
        async with get_async_session() as session:
            user_cmd = UserCommand(session)
            user = user_cmd.get_user(message.from_user.id)
            if user:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Введите город  или страну 🌍',
                                       reply_markup=kb_stop_fsm_weather())
                await WeatherStatWeek.city.set()

            else:
                await bot.send_message(chat_id=message.from_user.id, text=F"Пройдите регестрацию")
    except Exception as e:
        print(F"Ошибка при выборке пользователя")



@dp.message_handler(state=WeatherStatWeek.city)
async def get_weather_info(message: types.Message, state: FSMContext):
    """Обработка и вывов погоды на неделю"""
    city = message.text
    try:
        response = requests.get(
            url=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={APIWEATHER}&units=metric&lang=ru")
        data = response.json()

        # Получение текущей даты
        current_date = datetime.datetime.now().date()

        # Получение текущей даты
        current_date = datetime.datetime.now().date()

        # Словарь с соответствиями между номерами дней недели и их названиями на русском языке
        days_of_week = {
            0: 'Понедельник',
            1: 'Вторник',
            2: 'Среда',
            3: 'Четверг',
            4: 'Пятница',
            5: 'Суббота',
            6: 'Воскресенье'
        }

        # Создаем переменную для хранения сообщения с информацией о погоде
        weather_data = []

        # Итерация по каждому прогнозу погоды
        for forecast in data['list']:
            # Получение даты и времени прогноза
            forecast_date_time = datetime.datetime.fromtimestamp(forecast['dt'])
            forecast_date = forecast_date_time.date()
            forecast_time = forecast_date_time.time()

            # Проверка, является ли прогнозом на следующий день и полуденным
            if forecast_date > current_date and forecast_time.hour == 12:
                # Получение температуры полудня
                temperature = forecast['main']['temp']

                # Получение дня недели на русском языке
                day_of_week = days_of_week[forecast_date.weekday()]

                # Получение описания погодных условий
                weather_description = forecast['weather'][0]['description']


                # Формирование строки с информацией о погоде
                weather_info = f"<em>{day_of_week}</em>: <b>{temperature}°C </b><em>{weather_description}</em>"
                # Добавляем информацию в список
                weather_data.append(weather_info)
        weather_message = "\n".join(weather_data)
        # Отправляем фото и сообщение с информацией о погоде
        await bot.send_photo(chat_id=message.from_user.id,
                             caption=weather_message,
                             photo='https://www.google.com/imgres?imgurl=https%3A%2F%2Fotkrytkivsem.ru%2Fwp-content%2Fup'
                                   'loads%2F2021%2F03%2Fkartinka-dobrogo-dnya-i-horoshey-pogody.jpg&tbnid=fjxjmEGe36aCnM'
                                   '&vet=12ahUKEwiAw9G0-qH_AhUGpIsKHSniBLsQMyhFegQIARBt..i&imgrefurl=https%3A%2F%2Fotkryt'
                                   'kivsem.ru%2Fdlya-horoshego-nastroeniya%2Fdnevnye%2Fkartinka-dobrogo-dnya-i-horoshey-'
                                   'pogody%2F&docid=IWF1MG3_hiK-jM&w=600&h=600&q=%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0'
                                   '%BA%D0%B0%20%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0'
                                   '%B0%D1%82%D0%BD%D0%BE&ved=2ahUKEwiAw9G0-qH_AhUGpIsKHSniBLsQMyhFegQIARBt',
                             reply_markup=kb_weather())

        # Обнуляем список с данными о погоде
        weather_data.clear()
        await state.finish()
    except Exception as e:
        print(F"Ошибка при получении погоды: {e}")
        await message.answer(text=F"Такого города или страны не существует ☝️"
                                  F"Проверте корректность даных и попробуйте снова🙄",
                             reply_markup=kb_stop_fsm_weather())
