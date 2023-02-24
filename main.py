
import telebot
from battle.telegrambot.extensions import APIException, Convertor
from battle.telegrambot.config import TOKEN, exchanges
import traceback



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Привет, я твой карманный курс валют.\n По команде /help ты можешь ознакомиться с моими возможностями! "
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Для начала по команде /values ты можешь ознакомится с валютами которые я знаю,\n далее введи валюту которую хочешь перевести,\n после валюту в которую нужно перевести\nи в конце колличество"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
