from telebot import types

def main_menu():
    kb = types.InlineKeyboardMarkup() #Создаём разметку
    btn1 = types.InlineKeyboardButton(text="Доллар США🇺🇸", callback_data="USD")
    btn2 = types.InlineKeyboardButton(text="Евро🇪🇺", callback_data="EUR")
    btn3 = types.InlineKeyboardButton(text="Рос. рубль🇷🇺", callback_data="RUB")
    kb.add(btn1, btn2, btn3) # Добавляем кнопку в клавиатуру
    return kb