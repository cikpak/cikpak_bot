from telebot import types


def method_keyboard(locations):
    keyboard = types.ReplyKeyboardMarkup()
    if len(locations) != 0:
        for location in locations:
            keyboard.row(types.KeyboardButton(location))
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
