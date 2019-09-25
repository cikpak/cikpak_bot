from datetime import datetime
import re


def get_time_from_seconds(seconds):
	return datetime.fromtimestamp(seconds).strftime("%I:%M %p")


def deg_to_direction(deg):
	val = int((deg / 22.5) + .5)
	arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
	return arr[(val % 16)]


def is_city(city):
	return lambda: re.compile(r"[a-zA-Z]+(?:[ '-][a-zA-Z]+)*").fullmatch(city)


def format_wether_message(weather):
	return f"\
			🌡 Temperature\n\n Current  -  {weather['temp']} °C \
			\n\n--------------------------\n\n💨 Wind \n Speed  -   {weather['wind_speed']} Km/h  \n Direction  -  {deg_to_direction(weather['wind_deg'])}\
			\n\n--------------------------\n\n🌎 Atmosphere \n Pressure  -  {weather['pressure']} hPa \n Humidity  -  {weather['humidity']}%\
			\n\n--------------------------\n\n🌞 Sun\n Sunrise  -  {get_time_from_seconds(weather['sunrise'])} \n Sunset  -  {get_time_from_seconds(weather['sunset'])}\
			\n\n--------------------------\n\n 🌥 Clouds\n Clouds  -  {weather['clouds']} %"