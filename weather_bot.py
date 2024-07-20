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
    s = Sinoptik('Киев')
    res = ''
    time = 'ночь'
    a = s.get_data()[0]["weather_details"]["details"]
    if 'Температура, °C' in a:
        res += f"Температура в это время от {a['Температура, °C'][time][0]} °C до {a['Температура, °C'][time][1]} °C. "
    if 'чувствуется как ' in a:
        res += f"Чувствуется как {a['чувствуется как '][time][0]} °C до {a['чувствуется как '][time][1]} °C. "
    if 'Погода' in a and a['Погода'][time] != ['  ', '  ']:
        res += f"Погода в это время {a['Погода'][time][0]} - {a['Погода'][time][1]}. "
    if 'Влажность, %'  in a:
        res += f"Влажность: {a['Влажность, %'][time][0]} % до {a['Влажность, %'][time][1]} %. "
    if 'Вероятность осадков, %' in a and a['Вероятность осадков, %'][time] != ['-', '-']:
        res += f"Вероятность осадков: {a['Вероятность осадков, %'][time][0]} % до {a['Вероятность осадков, %'][time][1]} %. "

    bot.send_message(message.chat.id, f'{res}')


@bot.message_handler(commands=['temperature'])
def temperature(message):
    s = Sinoptik('Киев')
    bot.send_message(message.chat.id, f'Температура сегодня от {s.get_data()[0]["tMin"]} до {s.get_data()[0]["tMax"]}')


@bot.message_handler(commands=['week_temperature'])
def week_temperature(message):
    s = Sinoptik('Киев')
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
