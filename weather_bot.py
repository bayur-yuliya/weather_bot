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
    res = []
    time = 'ночь'
    a = s.get_data()[0]["weather_details"]["details"]
    if 'Температура, °C' in a:
        res.append('Температура, °C')
        res.append(a['Температура, °C'][time])
    if 'Погода' in a and a['Погода'][time] != ['  ', '  ']:
        res.append('Погода')
        res.append(a['Погода'][time])
    if 'чувствуется как ' in a:
        res.append('чувствуется как ')
        res.append(a['чувствуется как '][time])
    if 'Влажность, %'  in a:
        res.append('Влажность, %')
        res.append(a['Влажность, %'][time])
    if 'Вероятность осадков, %' in a and a['Вероятность осадков, %'][time] != ['-', '-']:
        res.append('Вероятность осадков, %')
        res.append(a['Вероятность осадков, %'][time])

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
