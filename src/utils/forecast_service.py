from pyowm import OWM
from config import weatherAPI
from datetime import datetime
from telebot.types import Location

obs = OWM(weatherAPI)

#TODO Forecast class can be better
class Forecast:
    def __init__(self, param):
        self.cast = {}
        self.forecast_by_days = {}
        try:
            if isinstance(param, str):
                self.location = param

                self.forecast = obs.three_hours_forecast(param).get_forecast()

            elif isinstance(param, Location):
                self.lat = param.latitude
                self.lon = param.longitude

                self.w = obs.three_hours_forecast_at_coords(lat=self.lat, lon=self.lon)

                self.forecast = w.get_forecast()

                self.location = w.get_location().get_name()
        except TypeError as e:
            print(e)

        self.divide_forecast_by_days()
        self.prepare_forecast()

    def divide_forecast_by_days(self):
        for part in self.forecast:
            if len(self.forecast_by_days.keys()) > 2:
                break
            day = datetime.fromtimestamp(part.get_reference_time()).date()
            if day not in self.forecast_by_days.keys():
                self.forecast_by_days[day] = []

            for part in list(self.forecast):
                try:
                    self.forecast_by_days[datetime.fromtimestamp(part.get_reference_time()).date()].append(part)
                except:
                    break

    def prepare_forecast(self):

        for day in self.forecast_by_days.keys():
            min = self.forecast_by_days[day][0].get_temperature(unit='celsius')['temp_min']
            max = self.forecast_by_days[day][0].get_temperature(unit='celsius')['temp_max']
            status = []

            for part in self.forecast_by_days[day]:

                if part.get_temperature(unit='celsius')['temp_min'] < min:
                    min = part.get_temperature(unit='celsius')['temp_min']

                if part.get_temperature(unit='celsius')['temp_max'] > max:
                    max = part.get_temperature(unit='celsius')['temp_max']

                status.append(part.get_detailed_status())

            self.cast[day] = {'min': round(min), 'max': round(max), 'status': status}

    def get_status_for_day(self, par: list):
        status_count = 0
        weather_status = ''

        for element in set(par):
            if par.count(element) > status_count:
                status_count = par.count(element)
                weather_status = element

        return weather_status

    def __str__(self):
        forecast_text = f"Forecast for {self.location.capitalize()}\n\n"
        for day in self.cast:
            status = self.get_status_for_day(self.cast[day]['status'])
            forecast_text += f'Day: {day}\nStatus: {status}\nMax: {self.cast[day]["max"]}\nMin: {self.cast[day]["min"]}\n\n'

        return forecast_text


    def get_location(self):
        return self.location