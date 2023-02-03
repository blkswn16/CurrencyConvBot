import telebot
from config import keys, TOKEN
from extensions import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n Используйте /currencies чтобы просмотреть возможные варианты валют'
    bot.reply_to(message, text)


@bot.message_handler(commands=['currencies'])
def currencies(message: telebot.types.Message) :
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConversionException('Слишком много параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(base, quote, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
