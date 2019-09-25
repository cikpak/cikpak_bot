import json

import requests

from config import weather_api as api_key


def format_weather_response(response):
	if response['cod'] == 200:
		print(json.dumps(response, indent=2))
		weather_info = {
			'temp': response['main']['temp'],
			'humidity': response['main']['humidity'],
			'pressure': response['main']['pressure'],
			'location': f"{response['name']},{response['sys']['country']}",
			'sunrise': response['sys']['sunrise'],
			'sunset': response['sys']['sunset'],
			'clouds': response['clouds']['all'],
			'wind_speed': response['wind']['speed'],
			'wind_deg': response['wind']['deg'],
			'weather_id': response['weather'][0]['main'],
			'city' : response['name'],
			'country': response['sys']['country']
		}
		return weather_info
	else:
		return NameError


def get_weather(city):
	url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

	return format_weather_response(requests.get(url).json())
