from pyowm import OWM
from config import weatherAPI
from datetime import datetime
from telebot.types import Location
from random import choice

obs = OWM(weatherAPI)


# TODO Forecast class can be better
class Forecast:
    def __init__(self, message, units):
        self.units = units
        self.cast = {}
        self.forecast_by_days = {}

        

        if not message.location:
            self.location = message.text.title()
            self.forecast = obs.three_hours_forecast(self.location).get_forecast()
        else:
            self.lat = message.location.latitude
            self.lon = message.location.longitude

            self.forecast = obs.three_hours_forecast_at_coords(self.lat, self.lon).get_forecast()
            self.location = self.forecast.get_location().get_name()

        self.divide_forecast_by_days()
        self.prepare_forecast()

    def divide_forecast_by_days(self):
        for part in list(self.forecast):
            if len(self.forecast_by_days.keys()) > 3:
                break
            day = datetime.fromtimestamp(part.get_reference_time()).date()
            if day not in self.forecast_by_days.keys():
                self.forecast_by_days[day] = []

            for part in self.forecast:
                try:
                    self.forecast_by_days[datetime.fromtimestamp(part.get_reference_time()).date()].append(part)
                except:
                    break
    
    def get_status_for_day(self, par: list):
        status_count = 0
        weather_status = ''

        for element in set(par):
            if par.count(element) > status_count:
                status_count = par.count(element)
                weather_status = element

        return weather_status

    def get_status_by_code(self, status):
        # TODO - fix blood from eyes
        status_as_emoji = {
            'clear': '☀️',
            'clouds': '⛅️',
            'shower rain': '🌦',
            'rain': '🌧',
            'thunderstorm': '⛈',
            'snow': '❄️',
            'drizzle': '🌧'
        }

        if int(status/100) == 8:
            if status == 800:
               return status_as_emoji['clear']
            else:
               return status_as_emoji['clouds']
        elif int(status/100) == 5:
            if status == 521:
               return status_as_emoji['shower rain']
            else:
               return status_as_emoji['rain']
        elif int(status/100) == 6:
           return status_as_emoji['snow']
        elif int(status/100) == 2:
           return status_as_emoji['thunderstorm']
        elif int(status/100) == 3:
           return status_as_emoji['drizzle']
        elif int(status/100) == 7:
           return status

    def prepare_forecast(self):
        unit = ''
        if self.units == 'C':
            unit = 'celsius'
        else:
            unit = 'fahrenheit'

        for day in list(self.forecast_by_days.keys())[1:]:
            min = self.forecast_by_days[day][0].get_temperature(unit=unit)[
                'temp_min']
            max = self.forecast_by_days[day][0].get_temperature(unit=unit)[
                'temp_max']

            status_arr = []

            for part in self.forecast_by_days[day]:
                if part.get_temperature(unit)['temp_min'] < min:
                    min = part.get_temperature(unit)['temp_min']

                if part.get_temperature(unit='celsius')['temp_max'] > max:
                    max = part.get_temperature(unit=unit)['temp_max']

                status = part.get_weather_code()
                status_arr.append(self.get_status_by_code(status))

            self.cast[day] = {'min': round(min), 'max': round(
                max), 'status': self.get_status_for_day(status_arr)}

    

    def __str__(self):
        forecast_text = f"Forecast for <b>{self.location.capitalize()}</b>\n\n"
        for day in self.cast:
            date = day.strftime('%A %d %b %Y')
            status = self.cast[day]['status']

            max = self.cast[day]["max"]
            min = self.cast[day]["min"]

            globe_emoji = choice(['🌍', '🌎', '🌏'])
            forecast_text += (
                f"{globe_emoji} <pre>  </pre><b>{date}</b>\n"
                f"-<b>Weather:</b> <pre>  </pre>{status}\n"
                f"-<b>Lowest temp:</b>  <pre>  </pre>{min} °{self.units}\n"
                f"-<b>Highest temp:</b> <pre>  </pre>{max} °{self.units}\n\n"
            )

        return forecast_text

    def get_location(self):
        return self.location
