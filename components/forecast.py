from utils.forecast_service import Forecast
from state import get_active_user
from keyboards import *
from main import bot
from main import remove_keyboard
import database.db_service as ds


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
