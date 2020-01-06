import telebot
from telebot import types
from config import TOKEN
import database.data_service.db_service as ds
from database.set_db import init_database
import utils.instruments as f
import state
from utils.forecast_service import get_forecast_by_city, get_forecast_by_location
from keyboards import current_keyboard, main_keyboard, settings_keyboard
from utils.weather_service import get_weather_by_coords, get_weather_by_city

bot = telebot.TeleBot(TOKEN)

remove_keyboard = types.ReplyKeyboardRemove()


@bot.message_handler(func=lambda message: message.text == 'Location')
def location_handler(message):
    bot.reply_to(message, 'Please send your current location')
    bot.register_next_step_handler(message, handle_location_weather)


def handle_location_weather(message):
    location = get_forecast_by_location(message.location)
    bot.send_message(message.chat.id, location)


@bot.message_handler(func=lambda message: message.text == 'Current')
def current_handler(message):
    bot.send_message(message.chat.id, 'Choose a option:', reply_markup=current_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Forecast')
def forecast_handler(message):
    bot.reply_to(message, "Enter city name (ex: New York:)")
    bot.register_next_step_handler(message, handle_forecast_request)


def handle_forecast_request(message):
    city = message.text
    forecast = get_forecast_by_city(city)
    bot.reply_to(message, forecast)


@bot.message_handler(func=lambda message: message.text == 'Settings')
def settings_handler(message):
    bot.send_message(message.chat.id, 'Settings', reply_markup=settings_keyboard())


@bot.message_handler(commands=['weather'])
def handle_weather(message):
    bot.send_message(message.chat.id, '/weather coming soon')


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


@bot.message_handler(func=lambda city, f=f.is_city: f(city))
def handle_message(message):
    print("city enter")
    weather = get_weather_by_city(message.text)
    if weather is not NameError:
        bot.send_message(message.chat.id, weather)
    else:
        bot.reply_to(message, f'Something is wrong, check city name and try again')


if __name__ == '__main__':
    init_database()
    bot.polling()
