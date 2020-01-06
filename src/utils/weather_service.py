from pyowm import OWM
from config import weatherAPI
from utils.instruments import format_weather_response

obs = OWM(weatherAPI)


# TODO - Rewrite Weather as a class

def get_weather_by_city(city):
    weather = obs.weather_at_place(city)
    return format_weather_response(weather)


def get_weather_by_coords(location):
    lat = location.latitude
    lon = location.longitude
    weather = obs.weather_at_coords(lat=lat, lon=lon)
    return format_weather_response(weather)
