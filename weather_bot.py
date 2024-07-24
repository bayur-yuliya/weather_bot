import telebot
import webbrowser

from config import secret_token
from generate_data import Sinoptik


API_TOKEN = secret_token
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                      f'Я - бот, который сможет помочь вам узнать погоду в вашем городе!')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://sinoptik.ua/', new=1)


@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        s = Sinoptik('Киев')
        weather_info = s.fetch_weather_data('Киев', 'ночь')
        bot.send_message(message.chat.id, weather_info)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при получении данных о погоде.')
        print(f'Произошла ошибка при получении данных о погоде: {str(e)}')



@bot.message_handler(commands=['temperature'])
def temperature(message):
    try:
        s = Sinoptik('Киев')
        data = s.get_data()[0]
        bot.send_message(message.chat.id, f'Температура сегодня от {data["tMin"]} до {data["tMax"]}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при получении данных о температуре: {str(e)}')


@bot.message_handler(commands=['week_temperature'])
def week_temperature(message):
    try:
        s = Sinoptik('Киев')
        week_data = [f"{el['day']}: {el['tMin']} - {el['tMax']}" for el in s.get_data()]
        bot.send_message(message.chat.id, f'Температура на неделю: {", ".join(week_data)}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка при получении данных на неделю: {str(e)}')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, """Я вас не понимаю. Попробуйте еще раз. """)


bot.infinity_polling()
