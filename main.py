import telebot
import threading
from telebot import types
from config import TOKEN
import importlib


bot = telebot.TeleBot(TOKEN)
remove_keyboard = types.ReplyKeyboardRemove()

import schedule
from utils.daily import daily_messages
from database.set_db import init_database
from state import get_active_user
from components.settings import *
from components.forecast import *
from components.weather import *


from keyboards import method_keyboard, main_keyboard, settings_keyboard
import database.db_service as ds


@bot.message_handler(func=lambda message: message.text == 'Back')
def back_handler(message):
    bot.send_message(message.chat.id, 'Main Menu', reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Current')
def by_city_handler(message):
    active_user = get_active_user(message.from_user.id)
    bot.reply_to(message, 'Send your location or enter city name', reply_markup=method_keyboard(active_user.locations))
    bot.register_next_step_handler(message, handle_weather)


@bot.message_handler(func=lambda message: message.text == 'Forecast')
def forecast_handler(message):
    active_user = get_active_user(message.from_user.id)
    bot.reply_to(message, 'Send your location or enter city name', reply_markup=method_keyboard(active_user.locations))
    bot.register_next_step_handler(message, handle_forecast)


@bot.message_handler(func=lambda message: message.text == 'Settings')
def settings_handler(message):
    bot.send_message(message.chat.id, 'Settings', reply_markup=settings_keyboard())


@bot.message_handler(commands=['start'])
def handle_start(message):
    active_user = ds.find_user_by_id(message.from_user.id)
    if not active_user:
        # collect new user info
        user_info = message.from_user
        telegram_id = user_info.id
        language = user_info.language_code
        username = user_info.username

        active_user = ds.create_user(telegram_id, username, language)

        bot.send_message(message.chat.id, f"Hello {active_user.username}, welcome to cikpak-weather-bot")
        bot.send_message(message.chat.id, 'By default you will receive weather in °C')
        bot.send_message(message.chat.id, 'You can change it in settings')
    else:
        bot.send_message(message.chat.id, f"Hello, {active_user.username}!")

    bot.send_message(message.chat.id, 'Choose a option:', reply_markup=main_keyboard())


def job():
    return daily_messages(bot)


def daily_weather_worker(self):
    schedule.run_pending()


if __name__ == '__main__':
    schedule.every(3).seconds.do(job)
    print('Starting database...')
    init_database()
    print('Succes!')
    print('--------------------')
    print('Bot Polling')
    thread = threading.Thread(target=daily_weather_worker, args=(1,))
    thread.start()
    bot.polling()
