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
    if message.text == 'Add location':
        bot.send_message(message.chat.id, 'Please send city name or your location do add it in your favourites!')
        bot.register_next_step_handler(message, add_location)
    else:
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

    #TODO can be better and easyer
    if message.text == 'Add location':
        bot.send_message(message.chat.id, 'Please send city name or your location do add it in your favourites!')
        bot.register_next_step_handler(message, add_location)
    else:
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


def add_location(message):
    #TODO can be better and easyer
    #TODO add location to user location in db
    if message.text != 'Back':
        try:
            city=''
            if message.location:
                #TODO find a way to get city name by coords without api call to owm
                weather = Weather(message.location)
                city = weather.get_location()
            else:
                city = message.text
            
            print(f'{city=}')
            #TODO redraw keyboard with user's location
        except:
            print('error')
    else:
        bot.send_message(message.chat.id, 'Main Menu', reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Units')
def settings_handler(message):
    bot.send_message(message.chat.id, 'Send C for celsius or F for farenheit')
    bot.register_next_step_handler(message, handle_units_choise)


def handle_units_choise(message):
    if message.text != 'Back':
        if message.text.capitalize() =='F' or message.text.capitalize() == 'C':
            print(f'{message.text=}')
            #TODO Rewrite user units in database

        else:
            bot.send_message(message.chat.id, 'Something is wrong, send again your choise!')
            bot.register_next_step_handler(message, handle_units_choise)
    else:
        bot.send_message(message.chat.id, 'Main Menu', reply_markup=main_keyboard())

    


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
