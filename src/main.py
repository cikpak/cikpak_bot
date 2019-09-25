import telebot
from telebot import types

from src.utils.weatherAPI import get_weather
from config import TOKEN
from src.utils.weatherDict import weather_id
import database.data_service.db_service as ds
from database.set_db import init_database
import utils.instruments as f
import state

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['sticker'])
def handle_stickers(message):
	print(message.sticker.file_id)


@bot.message_handler(func=lambda message: message.text.lower() == 'location')
def weather_handler(message):
	k = types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, 'something', reply_markup=k)
	bot.send_message(message.chat.id, 'Echo Location')


@bot.message_handler(func=lambda message: message.text.lower() == 'forecast')
def weather_handler(message):
	bot.send_message(message.chat.id, 'Echo forecast')


@bot.message_handler(func=lambda message: message.text.lower() == 'city')
def weather_handler(message):
	k = types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, 'something', reply_markup=k)


# bot.send_message(message.chat.id, 'Please enter your city name: ex: New York')


@bot.message_handler(content_types=['location'])
def handle_location(message):
	print(message.location)


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

	keyboard = types.ReplyKeyboardMarkup()

	location = types.KeyboardButton("Location")
	city = types.KeyboardButton('City')
	settings = types.KeyboardButton("Settings")

	keyboard.row(location, settings)
	keyboard.row(city)
	bot.send_message(message.chat.id, 'Choose a option:', reply_markup=keyboard)


@bot.message_handler(func=lambda city, f=f.is_city: f(city))
def handle_message(message):
	print("city enter")
	weather = get_weather(message.text)
	if weather is not NameError:
		bot.send_sticker(message.chat.id, weather_id[weather['weather_id']])
		bot.send_message(message.chat.id, f'{weather["city"]}, {weather["country"]} - {weather["weather_id"]}')
		response_text = f.format_wether_message(weather)
		bot.send_message(message.chat.id, response_text)
	else:
		bot.reply_to(message, f'Something is wrong, check city name and try again')


if __name__ == '__main__':
	init_database()
	bot.polling()
