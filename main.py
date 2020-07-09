import telebot
import threading
from telebot import types
import schedule
from utils.daily import daily_messages
from config import TOKEN
from database.set_db import init_database
from state import get_active_user
from utils.forecast_service import Forecast
from keyboards import method_keyboard, main_keyboard, settings_keyboard, user_locations, daily_weather
from utils.weather_service import Weather
import database.db_service as ds

bot = telebot.TeleBot(TOKEN)
remove_keyboard = types.ReplyKeyboardRemove()


@bot.message_handler(func=lambda message: message.text == 'Back')
def back_handler(message):
    bot.send_message(message.chat.id, 'Main Menu', reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Current')
def by_city_handler(message):
    print(message.chat.id)
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
            location = forecast.get_location().title()
            if location not in active_user.locations:
                ds.add_location(active_user.telegram_id, location)

                bot.reply_to(message, f'{location} was added to your favourites locations')
                bot.send_message(message.chat.id, str(forecast), parse_mode='HTML')
                bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())

            else:
                bot.send_message(message.chat.id, f'{location} is already in your locations list\n There is forecast')
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
        location = weather.get_location()
        if location not in active_user.locations:
            ds.add_location(active_user.telegram_id, location)

            bot.reply_to(message, f'{location} was added to your favourites locations')
            bot.send_message(message.chat.id, str(weather), parse_mode='HTML')
            bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=main_keyboard())
        else:
            bot.send_message(message.chat.id, f'{location} is already in your locations list')
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


@bot.message_handler(func=lambda message: message.text == 'Location')
def default_location_handler(message):
    active_user = get_active_user(message.from_user.id)
    bot.send_message(message.chat.id, f'Your current default location is -> {active_user.default_location}')

    bot.send_message(message.chat.id, 'You can choose another one from list above',
                     reply_markup=user_locations(active_user.locations))
    bot.register_next_step_handler(message, handle_default_location_choise)


def handle_default_location_choise(message):
    active_user = get_active_user(message.from_user.id)
    if message.text != 'Back':
        new_location = message.text
        ds.set_default_location(active_user.telegram_id, new_location)
        bot.send_message(message.chat.id, f'Your new default location is {new_location}', reply_markup=main_keyboard())
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

        active_user = ds.create_user(telegram_id, username, language)

        bot.send_message(message.chat.id, f"Hello {active_user.username}, welcome to cikpak-weather-bot")
        bot.send_message(message.chat.id, 'By default you will receive weather in °C')
        bot.send_message(message.chat.id, 'You can change it in settings')
    else:
        bot.send_message(message.chat.id, f"Hello, {active_user.username}!")

    bot.send_message(message.chat.id, 'Choose a option:', reply_markup=main_keyboard())


@bot.message_handler(func=lambda message: message.text == 'Daily weather')
def daily_weather_handler(message):
    active_user = get_active_user(message.from_user.id)

    if active_user.subscribed:
        bot.send_message(message.chat.id,
                         f'You are subscribed to daily weather, your default city is {active_user.default_location}',
                         reply_markup=daily_weather(active_user.subscribed))
        bot.register_next_step_handler(message, handle_subscribe_choise)
    else:
        bot.send_message(message.chat.id, 'You are not subscribed to daily weather :(',
                         reply_markup=daily_weather(active_user.subscribed))
        bot.register_next_step_handler(message, handle_subscribe_choise)


def handle_subscribe_choise(message):
    active_user = get_active_user(message.from_user.id)

    if message.text != 'Back':
        user = ds.change_user_subscribtion(active_user.telegram_id)

        if message.text == "Subscribe":
            bot.send_message(message.chat.id, 'You subscribed succesfuly to daily weather!')
            bot.send_message(message.chat.id, 'You will receive daily weather at 8 AM!',
                             reply_markup=main_keyboard())
        else:
            bot.send_message(message.chat.id, 'You unsubscribed succesfuly from daily weather!')
            bot.send_message(message.chat.id, 'You will not receive daily weather anymore!',
                             reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id, 'Returned to main Menu', reply_markup=settings_keyboard())


def job():
    return daily_messages(bot)


def daily_weather_worker(self):
    while True:
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
