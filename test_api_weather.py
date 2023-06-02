
from data.config import APIWEATHER
import datetime

import requests
from pprint import pprint
from datetime import datetime, timedelta


def get_weather(city, API_key):
    try:
        response = requests.get(
            url=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_key}&units=metric&lang=ua")
        data = response.json()

        # Получение текущей даты
        current_date = datetime.now().date()

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

        # Итерация по каждому прогнозу погоды
        for forecast in data['list']:
            # Получение даты и времени прогноза
            forecast_date_time = datetime.fromtimestamp(forecast['dt'])
            forecast_date = forecast_date_time.date()
            forecast_time = forecast_date_time.time()

            # Проверка, является ли прогнозом на следующий день и полуденным
            if forecast_date > current_date and forecast_time.hour == 12:
                # Получение температуры полудня
                temperature = forecast['main']['temp']

                # Получение дня недели на русском языке
                day_of_week = days_of_week[forecast_date.weekday()]

                # Вывод температуры и дня недели
                print(f"Температура в {city} в {day_of_week}: {temperature}°C")

    except Exception as e:
        pprint(f"Ошибка: {e}")


def main():
    get_weather('харьков', APIWEATHER)


if __name__ == '__main__':
    main()

# def get_weather(city, open_weather_token):
#     try:
#         code_to_smile = {
#             "Clear": "Ясно \U00002600",
#             "Clouds": "Облачно \U00002601",
#             "Rain": "Дождь \U00002614",
#             "Drizzle": "Дождь \U00002614",
#             "Thunderstorm": "Гроза \U000026A1",
#             "Snow": "Снег \U0001F328",
#             "Mist": "Туман \U0001F32B"
#         }
#         r = requests.get(
#             F"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ua,uk"
#         )
#         data=r.json()
#         city_name = data['name']
#         min_temp = data['main']['temp_min']
#         weather_description = data["weather"][0]["main"]
#         if weather_description in code_to_smile:
#             wd = code_to_smile[weather_description]
#         else:
#             wd = "Посмотри в окно, не пойму что там за погода!"
#         temp = data['main']['temp']
#         max_temp = data['main']['temp_max']
#         country = data['sys']['country']
#         humidity=data['main']['humidity']
#         pressure=data['main']['pressure']
#         speed_wind=data['wind']['speed']
#         sunrise=datetime.datetime.fromtimestamp(data['sys']['sunrise'])
#         sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
#         length_of_the_day=sunset-sunrise
#         print(F'погода в городе : {city_name} \n'
#               F'***Текущая дата :{datetime.datetime.now().date()}*** \n'
#               F'Текущая температура : {temp}°C {wd} \n'
#               F'Минимальная температура : {min_temp}°C \n'
#               F'Максимальная температура : {max_temp} °C\n'
#               F'Страна : {country} \n'
#               F'Влажность : {humidity} \n'
#               F'Давления : {pressure} мм.рт.ст\n'
#               F'Скорость ветра : {speed_wind} м/с \n'
#               F'Рассвет : {sunrise} \n'
#               F'Закат : {sunset} \n'
#               F'Продолжительность дня : {length_of_the_day} \n'
#               F'Хорошего дня '
#               )
#         # pprint(data)
#     except Exception as e:
#         pprint(F"Ошибка :{e}")
#
#
# def main():
#     city = input("Введите город :")
#     get_weather(city, APIWEATHER)
#
#
# if __name__ == '__main__':
#     main()
