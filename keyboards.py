from telebot import types
from database.user import User


def method_keyboard(locations: list) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup()
    if len(locations) != 0:
        for location in locations:
            keyboard.row(types.KeyboardButton(location))
    add = types.KeyboardButton("Add location")
    back = types.KeyboardButton('Back')

    keyboard.row(add, back)

    return keyboard


def main_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup()

    location = types.KeyboardButton("Current")
    city = types.KeyboardButton('Forecast')
    settings = types.KeyboardButton("Settings")

    keyboard.row(location, city)
    keyboard.row(settings)

    return keyboard


def settings_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup()

    units = types.KeyboardButton('Units')
    default_location = types.KeyboardButton('Location')
    daily_weather = types.KeyboardButton('Daily weather')
    back = types.KeyboardButton('Back')

    keyboard.row(units, daily_weather)
    keyboard.row(default_location)
    keyboard.row(back)

    return keyboard


def user_locations(locations: list) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup()

    if len(locations) != 0:
        for location in locations:
            keyboard.row(types.KeyboardButton(location))

    back = types.KeyboardButton('Back')
    keyboard.row(back)

    return keyboard


def daily_weather(isSubscribed: bool) -> User:
    keyboard = types.ReplyKeyboardMarkup()

    if isSubscribed:
        keyboard.row(types.KeyboardButton('Unsubscribe'))
    else:
        keyboard.row(types.KeyboardButton('Subscribe'))

    back = types.KeyboardButton('Back')
    keyboard.row(back)

    return keyboard
