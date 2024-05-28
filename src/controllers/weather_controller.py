from datetime import datetime
from typing import List
import pandas as pd
from src.entity.city import City
from src.entity.weather import WeatherDay
from meteostat import Monthly, Point
from geopy.geocoders import Nominatim


class WeatherController:
    @classmethod
    def create_weather_objects(cls, weather_data: dict) -> List[WeatherDay]:
        weather_objects = []
        for day in weather_data['days']:
            weather_day = WeatherDay(
                datetime=day['datetime'],
                temp_max=day['tempmax'],
                temp_min=day['tempmin'],
                feels_like=day['feelslike'],
                precip_prob=day['precipprob'],
                wind_speed=day['windspeed'],
                conditions=day['conditions'],
                icon=day['icon']
            )
            weather_objects.append(weather_day)
        return weather_objects

    @classmethod
    def get_average_weather(cls):
        # user_residence: City, departure_date: str, return_date: str
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode("tel aviv")
        if location:

            start_month = pd.Period(year=2023, month=5, freq='M')
            end_month = pd.Period(year=2023, month=5, freq='M')
            start = start_month.start_time
            end = end_month.end_time
            point = Point(location.latitude, location.longitude)
            data = Monthly(point, start, end)
            data = data.fetch()
            average_temp = data['tavg']
            average_temp_dict = average_temp.dropna().to_dict()
            average_temp_dict_str = {date.strftime('%Y-%m-%d'): temp for date, temp in average_temp_dict.items()}

            print(average_temp_dict_str)
