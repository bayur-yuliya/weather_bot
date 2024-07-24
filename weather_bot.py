import telebot
import webbrowser

from config import secret_token
from generate_data import Sinoptik


API_TOKEN = secret_token
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                      f'Я - бот, который поможет вам узнать погоду в вашем городе! '
                                      f'Пожалуйста, укажите ваш город командой /city <название города>')

@bot.message_handler(commands=['city'])
def set_city(message):
    try:
        city = message.text.split()[1]
        user_data[message.chat.id] = city
        bot.send_message(message.chat.id, f'Город установлен: {city}')
    except IndexError:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите город в формате: /city <название города>')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://sinoptik.ua/', new=1)


@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        city = user_data.get(message.chat.id)
        s = Sinoptik(city)
        weather_info = s.fetch_weather_data(city, 'ночь')
        bot.send_message(message.chat.id, weather_info)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при получении данных о погоде.')
        print(f'Произошла ошибка при получении данных о погоде: {str(e)}')


@bot.message_handler(commands=['temperature'])
def temperature(message):
    try:
        s = Sinoptik(user_data.get(message.chat.id))
        data = s.get_data()[0]
        bot.send_message(message.chat.id, f'Температура сегодня от {data["tMin"]} до {data["tMax"]}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при получении данных о температуре: {str(e)}')


@bot.message_handler(commands=['week_temperature'])
def week_temperature(message):
    try:
        s = Sinoptik(user_data.get(message.chat.id))
        week_data = [f"{el['day']}: {el['tMin']} - {el['tMax']}" for el in s.get_data()]
        bot.send_message(message.chat.id, f'Температура на неделю: {", ".join(week_data)}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при получении данных на неделю.')
        print(f'Произошла ошибка при получении данных на неделю: {str(e)}')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, """Я вас не понимаю. Попробуйте еще раз. """)


bot.infinity_polling()
