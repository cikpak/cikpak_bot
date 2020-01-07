from telebot import types


def method_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    add = types.KeyboardButton("Add location")
    back = types.KeyboardButton('Back')

    keyboard.row(add, back)

    return keyboard


def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    location = types.KeyboardButton("Current")
    city = types.KeyboardButton('Forecast')
    settings = types.KeyboardButton("Settings")

    keyboard.row(location, city)
    keyboard.row(settings)

    return keyboard


def settings_keyboard():
    keyboard = types.ReplyKeyboardMarkup()

    units = types.KeyboardButton('Units')
    back = types.KeyboardButton('Back')

    keyboard.row(units)
    keyboard.row(back)

    return keyboard
