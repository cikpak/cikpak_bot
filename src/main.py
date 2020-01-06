import telebot
from telebot import types
from config import TOKEN
import database.data_service.db_service as ds
from database.set_db import init_database
from utils.instruments import is_city
import state
from utils.forecast_service import Forecast
from keyboards import method_keyboard, main_keyboard, settings_keyboard
from utils.weather_service import Weather

bot = telebot.TeleBot(TOKEN)
remove_keyboard = types.ReplyKeyboardRemove()


@bot.message_handler(func=lambda message: message.text == 'Back')
def back_handler(message):
    bot.send_message(message.chat.id, 'Main Menu', reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Current')
def by_city_handler(message):
    bot.reply_to(message, 'Send your location or enter city name', reply_markup=method_keyboard())
    bot.register_next_step_handler(message, handle_weather)


def handle_weather(message):
    try:
        weather = Weather(message.text)
        bot.send_message(message.chat.id, str(weather))
    except:
        try:
            weather = Weather(message.location)
            bot.send_message(message.chat.id, str(weather))
        except:
            bot.reply_to(message, f'Something is wrong, check city name and try again')
            bot.register_next_step_handler(message, handle_weather)


@bot.message_handler(func=lambda message: message.text == 'Forecast')
def forecast_handler(message):
    bot.reply_to(message, 'Send your location or enter city name', reply_markup=method_keyboard())
    bot.register_next_step_handler(message, handle_forecast)


def handle_forecast(message):
    try:
        forecast = Forecast(message.text)
        bot.send_message(message.chat.id, str(forecast))
    except:
        try:
            forecast = Forecast(message.location)
            bot.send_message(message.chat.id, str(forecast))
        except:
            bot.reply_to(message, f'Something is wrong, check city name and try again')
            bot.register_next_step_handler(message, handle_forecast)


@bot.message_handler(func=lambda message: message.text == 'Settings')
def settings_handler(message):
    bot.send_message(message.chat.id, 'Settings', reply_markup=settings_keyboard())


# @bot.message_handler(commands=['weather'])
# def handle_weather(message):
#     bot.send_message(message.chat.id, '/weather coming soon')


@bot.message_handler(commands=['start'])
def handle_start(message):
    state.active_user = ds.find_user_by_id(message.from_user.id)
    if not state.active_user:
        # collect new user info
        user_info = message.from_user
        telegram_id = user_info.id
        name = user_info.first_name
        lastname = user_info.last_name
        language = user_info.language_code
        username = user_info.username

        # create new user
        user = ds.create_user(telegram_id, name, lastname, username, language)
        state.active_user = user
        bot.send_message(message.chat.id, f"Hello {user.username}, welcome to cikpak-weather-bot")

    else:
        bot.send_message(message.chat.id, f"Hello, {state.active_user.username}!")

    bot.send_message(message.chat.id, 'Choose a option:', reply_markup=main_keyboard())


if __name__ == '__main__':
    init_database()
    bot.polling()
