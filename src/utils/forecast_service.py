from pyowm import OWM
from config import weatherAPI
from datetime import datetime
from utils.instruments import format_forecast_response

obs = OWM(weatherAPI)


# TODO Rewrite forecast ass a class

def prepare_forecast(forecast_by_days):
    forecast = {}

    for day in forecast_by_days.keys():
        min = forecast_by_days[day][0].get_temperature(unit='celsius')['temp_min']
        max = forecast_by_days[day][0].get_temperature(unit='celsius')['temp_max']
        status = []

        for part in forecast_by_days[day]:

            if part.get_temperature(unit='celsius')['temp_min'] < min:
                min = part.get_temperature(unit='celsius')['temp_min']

            if part.get_temperature(unit='celsius')['temp_max'] > max:
                max = part.get_temperature(unit='celsius')['temp_max']

            status.append(part.get_detailed_status())

        forecast[day] = {'min': round(min), 'max': round(max), 'status': status}
    return forecast


def divide_forecast_by_days(forecast):
    forecast_by_days = {}

    for part in forecast:
        if len(forecast_by_days.keys()) > 2:
            break
        day = datetime.fromtimestamp(part.get_reference_time()).date()
        if day not in forecast_by_days.keys():
            forecast_by_days[day] = []

        for part in list(forecast):
            try:
                forecast_by_days[datetime.fromtimestamp(part.get_reference_time()).date()].append(part)
            except:
                break

    return forecast_by_days


def get_forecast_by_city(city):
    forecast = obs.three_hours_forecast(city).get_forecast()
    forecast_by_days = divide_forecast_by_days(forecast)
    stats_by_day = prepare_forecast(forecast_by_days)

    city_name = forecast.get_location().get_name()

    return format_forecast_response(stats_by_day, city_name)


def get_forecast_by_location(location):
    lat = location.latitude
    lon = location.longitude

    forecast = obs.three_hours_forecast_at_coords(lat=lat, lon=lon).get_forecast()
    forecast_by_days = divide_forecast_by_days(forecast)
    stats_by_day = prepare_forecast(forecast_by_days)

    city_name = forecast.get_location().get_name()

    return format_forecast_response(stats_by_day, city_name)
