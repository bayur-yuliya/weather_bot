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


@bot.message_handler(commands=['temperature'])
def temperature(message):
    s = Sinoptik('Одесса')
    bot.send_message(message.chat.id, f'Температура сегодня от {s.get_data()[0]["tMin"]} до {s.get_data()[0]["tMax"]}')


@bot.message_handler(commands=['week_temperature'])
def week_temperature(message):
    s = Sinoptik('Одесса')
    a = []
    for el in s.get_data():
        a.append(el['day'] + ': ' + el['tMin'] + " - " + el['tMax'])
    bot.send_message(message.chat.id, f'Температура на неделю: {", ".join(a)}')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, """Я вас не понимаю. Попробуйте еще раз. """)


bot.infinity_polling()
