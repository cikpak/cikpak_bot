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


def format_weather_response(response):
    weather = response.get_weather()
    city = response.get_location().get_name()
    temp = round(weather.get_temperature(unit='celsius')['temp'])
    clouds = weather.get_clouds()
    weather = weather.get_status()
    formated_response = f'There is the weather for {city}\n\nTemperature:  {temp}°C\n Weather:  {weather}\n Clouds:  {clouds}'

    return formated_response


def get_status_for_day(list: list) -> str:
    status_count = 0
    weather_status = ''

    for element in set(list):
        if list.count(element) > status_count:
            status_count = list.count(element)
            weather_status = element

    return weather_status


def format_forecast_response(forecast, city: str):
    forecast_text = f"Forecast for {city.capitalize()}\n\n"
    for day in forecast:
        status = get_status_for_day(forecast[day]['status'])
        forecast_text += f'Day: {day}\nStatus: {status}\nMax: {forecast[day]["max"]}\nMin: {forecast[day]["min"]}\n\n'

    return forecast_text
