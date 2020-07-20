from database.user import User
from utils.weather_service import Weather
import telebot


def daily_messages(bot: telebot.TeleBot):
    users = User.objects(subscribed=True)

    for user in users:
        weather = Weather(user.default_location, user.units)
        bot.send_message(user.chat_id, str(weather), parse_mode='HTML')
