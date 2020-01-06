from telebot import types


def current_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    location = types.KeyboardButton("By location")
    city = types.KeyboardButton("By city")
    add = types.KeyboardButton("Add location")

    keyboard.row(location, city)
    keyboard.row(add)

    return keyboard


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    location = types.KeyboardButton("Current")
    city = types.KeyboardButton('Forecast')
    settings = types.KeyboardButton("Settings")

    keyboard.row(location, settings)
    keyboard.row(city)

    return keyboard


def settings_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    units = types.KeyboardButton('Units')
    back = types.KeyboardButton('back')

    keyboard.row(units)
    keyboard.row(back)

    return keyboard
