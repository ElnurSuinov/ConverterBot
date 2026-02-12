import telebot
import requests
from buttons import main_menu

bot = telebot.TeleBot('TELEGRAM_BOT_TOKEN')

# Получаем курсы валют из ЦентроБанка
def get_rates():
    url = "https://cbu.uz/ru/arkhiv-kursov-valyut/json/"
    response = requests.get(url)
    data = response.json()
    rates = {}
    for item in data:
        if item['Ccy'] in ['USD', 'EUR', 'RUB']:
            rates[item['Ccy']] = float(item['Rate'])
    return rates

# Храним выбор валюты нашего пользователя
user_currency_choice = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Выберите валюту, в которую хотите перевести:",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'EUR', 'RUB'])
def currency_choice(call):
    user_currency_choice[call.message.chat.id] = call.data
    bot.answer_callback_query(call.id)  # закрываем "часики" на кнопке
    bot.send_message(call.message.chat.id, "Введите сумму в узбекских сумах для конвертации:")

@bot.message_handler(func=lambda message: message.chat.id in user_currency_choice)
def convert_currency(message):
    try:
        amount = float(message.text)
        currency = user_currency_choice[message.chat.id]
        rates = get_rates()
        if currency in rates:
            result = amount / rates[currency]
            bot.send_message(message.chat.id, f"{amount} UZS🇺🇿 = {result:.2f} {currency}")
        else:
            bot.send_message(message.chat.id, "Курс валюты не найден.")
        del user_currency_choice[message.chat.id]
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректное число.")

bot.polling(non_stop=True)