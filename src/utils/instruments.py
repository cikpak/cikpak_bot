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







