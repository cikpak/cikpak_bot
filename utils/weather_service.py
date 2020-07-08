from pyowm import OWM
from config import weatherAPI
from random import choice

obs = OWM(weatherAPI)


# TODO - weather class can be better


class Weather:
    def __init__(self, message, units):
        print('init')
        self.units = units

        if units == 'C':
            temp_unit = 'celsius'
        else:
            temp_unit = 'fahrenheit'

        if not message.location:
            self.location = message.text.title()
            print(message)

            weather = obs.weather_manager().weather_at_place(message.text).weather
            self.temp = round(weather.temperature(unit=temp_unit)['temp'])

            print(weather.temperature)
            self.clouds = weather.clouds
            self.status_code = weather.weather_code
        else:
            lat = message.location.latitude
            lon = message.location.longitude
            weather = obs.weather_manager().weather_at_coords(lat=lat, lon=lon)

            self.location = weather.location.name
            self.temp = round(weather.weather.temperature(unit=temp_unit)['temp'])
            self.status_code = weather.weather.weather_code
            self.clouds = weather.weather.clouds

    def get_status(self):
        status = self.status_code
        status_as_emoji = {
            'clear': '☀️',
            'clouds': '⛅️',
            'shower rain': '🌦',
            'rain': '🌧',
            'thunderstorm': '⛈',
            'snow': '❄️',
            'drizzle': '🌧'
        }

        if int(status / 100) == 8:
            if status == 800:
                return status_as_emoji['clear']
            else:
                return status_as_emoji['clouds']
        elif int(status / 100) == 5:
            if status == 521:
                return status_as_emoji['shower rain']
            else:
                return status_as_emoji['rain']
        elif int(status / 100) == 6:
            return status_as_emoji['snow']
        elif int(status / 100) == 2:
            return status_as_emoji['thunderstorm']
        elif int(status / 100) == 3:
            return status_as_emoji['drizzle']
        elif int(status / 100) == 7:
            return 'something'

    def __str__(self):
        status = self.get_status()
        globe_emoji = choice(['🌍', '🌎', '🌏'])
        return (
            f'{globe_emoji}<pre>  </pre>The weather for <b>{self.location}</b> is:\n\n'
            f'-<b>Temperature</b>:<pre>  </pre>{self.temp}°{self.units}\n'
            f'-<b>Weather</b>: <pre>  </pre>{status}\n'
            f'-<b>Cloudiness</b>: <pre>  </pre>{self.clouds}%'
        )

    def get_location(self):
        return self.location
