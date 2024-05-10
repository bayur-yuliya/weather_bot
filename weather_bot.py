import telebot
import webbrowser

from config import secret_token


API_TOKEN = secret_token
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://sinoptik.ua/')


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Погода сегодня: ясно')


@bot.message_handler(commands=['temperature'])
def weather(message):
    bot.send_message(message.chat.id, 'Температура сейчас: тепло')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, """Я вас не понимаю. Попробуйте еще раз. """)


bot.infinity_polling()
