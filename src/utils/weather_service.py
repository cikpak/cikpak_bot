from pyowm import OWM
from config import weatherAPI
from telebot.types import Location

obs = OWM(weatherAPI)


class Weather:
    def __init__(self, param):
        try:
            if isinstance(param, str):
                self.city = param

                self.weather = obs.weather_at_place(self.city).get_weather()

                self.temp = round(self.weather.get_temperature(unit='celsius')['temp'])
                self.status = self.weather.get_status()
                self.clouds = self.weather.get_clouds()
            elif isinstance(param, Location):
                self.lat = param.latitude
                self.lon = param.longitude

                self.w = obs.weather_at_coords(lat=self.lat, lon=self.lon)
                self.weather = self.w.get_weather()

                self.city = self.w.get_location().get_name()
                self.temp = round(self.weather.get_temperature(unit='celsius')['temp'])
                self.status = self.weather.get_status()
                self.clouds = self.weather.get_clouds()
        except TypeError as e:
            print(e)

    def __str__(self):
        return f'There is the weather for {self.city}\n\nTemperature:  {self.temp}°C\n Weather:  {self.status}\n Clouds:  {self.clouds}'
