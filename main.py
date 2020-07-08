import telebot
from telebot import types
from config import TOKEN
from database.set_db import init_database
from state import get_active_user
from utils.forecast_service import Forecast
from keyboards import method_keyboard, main_keyboard, settings_keyboard
from utils.weather_service import Weather
import database.db_service as ds

bot = telebot.TeleBot(TOKEN)
remove_keyboard = types.ReplyKeyboardRemove()


@bot.message_handler(func=lambda message: message.text == 'Back')
def back_handler(message):
    bot.send_message(message.chat.id, 'Main Menu', reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Current')
def by_city_handler(message):
    active_user = get_active_user(message.from_user.id)
    print(active_user)
    bot.reply_to(message, 'Send your location or enter city name', reply_markup=method_keyboard(active_user.locations))
    bot.register_next_step_handler(message, handle_weather)


def handle_weather(message):
    if message.text == 'Add location':
        bot.reply_to(message, 'Send your location or city name to add it to favourites!', reply_markup=remove_keyboard)
        bot.register_next_step_handler(message, add_location_with_weather)
    elif message.text == 'Back':
        bot.send_message(message.chat.id, 'Main Menu', reply_markup=main_keyboard())
    else:
        try:
            active_user = get_active_user(message.from_user.id)
            weather = Weather(message, active_user.units)
            bot.send_message(message.chat.id, str(weather), parse_mode='HTML')
            bot.send_message(message.chat.id, 'Return to main Menu', reply_markup=main_keyboard())
        except Exception as e:
            print(e)
            bot.reply_to(message, f'Something is wrong, check city name and try again')
            bot.register_next_step_handler(message, handle_weather)


@bot.message_handler(func=lambda message: message.text == 'Forecast')
def forecast_handler(message):
    active_user = get_active_user(message.from_user.id)
    bot.reply_to(message, 'Send your location or enter city name', reply_markup=method_keyboard(active_user.locations))
    bot.register_next_step_handler(message, handle_forecast)


def handle_forecast(message):
    active_user = get_active_user(message.from_user.id)
    if message.text == 'Add location':
        bot.reply_to(message, 'Send your location or city name to add it to favourites!', reply_markup=remove_keyboard)
        bot.register_next_step_handler(message, add_location_with_forecast)
    elif message.text == 'Back':
        bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
    else:
        try:
            forecast = Forecast(message, active_user.units)
            bot.send_message(message.chat.id, str(forecast), parse_mode='HTML')
            bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
        except Exception as e:
            print(e)
            bot.reply_to(message, f'Something is wrong, check city name and try again')
            bot.register_next_step_handler(message, handle_forecast)


@bot.message_handler(func=lambda message: message.text == 'Settings')
def settings_handler(message):
    bot.send_message(message.chat.id, 'Settings', reply_markup=settings_keyboard())


def add_location_with_forecast(message):
    try:
        active_user = get_active_user(message.from_user.id)
        print(active_user)

        if message.text != 'Back':
            forecast = Forecast(message, active_user.units)
            city = forecast.get_location()
            if city not in active_user.locations:
                active_user.locations.append(city.title())
                active_user.save()

                bot.reply_to(message, f'{city} was added to your favourites locations')
                bot.send_message(message.chat.id, str(forecast), parse_mode='HTML')
                bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())

            else:
                bot.send_message(message.chat.id, f'{city} is already in your locations list\n There is forecast')
                bot.send_message(message.chat.id, str(forecast), parse_mode='HTML')
                bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
        else:
            bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
    except Exception as e:
        print(e)

def add_location_with_weather(message):
    active_user = get_active_user(message.from_user.id)
    if message.text != 'Back':
        weather = Weather(message, active_user.units)
        city = weather.get_location()
        print(city)
        if city not in active_user.locations:
            active_user.locations.append(city)
            active_user.save()

            bot.reply_to(message, f'{city} was added to your favourites locations')
            bot.send_message(message.chat.id, str(weather), parse_mode='HTML')
            bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
        else:
            bot.send_message(message.chat.id, f'{city} is already in your locations list')
            bot.send_message(message.chat.id, str(weather), parse_mode='HTML')
            bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Units')
def units_handler(message):
    active_user = get_active_user(message.from_user.id)
    bot.send_message(message.chat.id, f'Your curent units -> {active_user.units}')
    bot.send_message(message.chat.id, 'Send C for celsius or F for farenheit')
    bot.register_next_step_handler(message, handle_units_choise)


def handle_units_choise(message):
    active_user = get_active_user(message.from_user.id)
    new_units = message.text.title()
    if message.text != 'Back':
        if new_units in ['C', 'F']:
            if new_units != active_user.units:
                active_user.units = message.text.title()
                active_user.save()
                bot.send_message(message.chat.id, f'Now you will receive weather in °{message.text}')
                bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
            else:
                bot.send_message(message.chat.id, f'Your already receive weather and forecast in °{message.text}')
                bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
        else:
            bot.send_message(message.chat.id, 'Something is wrong, send again or verify entered units!')
            bot.register_next_step_handler(message, handle_units_choise)
    else:
        bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())


@bot.message_handler(commands=['start'])
def handle_start(message):
    active_user = ds.find_user_by_id(message.from_user.id)
    if not active_user:
        # collect new user info
        user_info = message.from_user
        telegram_id = user_info.id
        language = user_info.language_code
        username = user_info.username

        print(active_user)
        active_user = ds.create_user(telegram_id, username, language)

        bot.send_message(message.chat.id, f"Hello {active_user.username}, welcome to cikpak-weather-bot")
        bot.send_message(message.chat.id, 'By default you will receive weather in °C')
        bot.send_message(message.chat.id, 'You can change it in settings')

    else:
        bot.send_message(message.chat.id, f"Hello, {active_user.username}!")

    bot.send_message(message.chat.id, 'Choose a option:', reply_markup=main_keyboard())


if __name__ == '__main__':
    print('Starting database...')
    init_database()
    print('Succes!')
    print('--------------------')
    print('Bot Polling')
    bot.polling()
