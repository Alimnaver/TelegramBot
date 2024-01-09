import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot("")
currency = CurrencyConverter
meaning = 0


@bot.message_handler(commands={"help"})
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который конвертирует интересующую тебя валюту. Чтобы начать работу со мной, нажми /start, затем введи сумму, которую нужно сконвертировать. После этого выбери интересующую тебя валюту или введи её самостоятельно")
    bot.register_next_step_handler(message, summa)


@bot.message_handler(commands={"start"})
def start(message):
    bot.send_message(message.chat.id, "Привет, введите сумму")
    bot.register_next_step_handler(message, summa)


def summa(message):
    global meaning
    try:
        meaning = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат, введите сумму")
        bot.register_next_step_handler(message, summa)
        return

    if meaning > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("RUB/USD", callback_data="rub/usd")
        btn2 = types.InlineKeyboardButton("USD/RUB", callback_data="usd/rub")

        btn3 = types.InlineKeyboardButton("RUB/EUR", callback_data="rub/eur")
        btn4 = types.InlineKeyboardButton("EUR/RUB", callback_data="eur/rub")

        btn5 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn6 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")

        btn7 = types.InlineKeyboardButton("KGS/USD", callback_data="kgs/usd")
        btn8 = types.InlineKeyboardButton("USD/KGS", callback_data="usd/kgs")

        btn9 = types.InlineKeyboardButton("KGS/EUR", callback_data="kgs/eur")
        btn10 = types.InlineKeyboardButton("EUR/KGS", callback_data="eur/kgs")

        btn11 = types.InlineKeyboardButton("Другая валюта", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
        bot.send_message(message.chat.id, "Выберите пару валют", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число должно быть больше 0")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != "else":
        values = call.data.upper().split("/")
        res = currency.convert(meaning, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Получается: {round(res, 2)}. Можете заново писать сумму")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id,"Введите пару интересуемых вас валют через слэш(/)")
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split("/")
        res = currency.convert(meaning, values[0], values[1])
        bot.send_message(message.chat.id, f"Получается: {round(res, 2)}. Можете заново писать сумму")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, "Что то пошло не так, впишите значение заново")
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)