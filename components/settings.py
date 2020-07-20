from keyboards import *
from state import get_active_user
import database.db_service as ds
from main import bot



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
