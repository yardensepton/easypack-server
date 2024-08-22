from datetime import datetime
from typing import List
import pandas as pd

from src.enums.user_weather_feeling_options import UserWeatherFeelingOptions
from src.models.weather import WeatherDay
from meteostat import Monthly, Point


class WeatherController:
    @classmethod
    def create_weather_objects(cls, weather_data: dict) -> List[WeatherDay]:
        """
               Create a list of WeatherDay objects from raw weather data.

               Args:
                   weather_data (dict): Raw weather data containing daily weather information.

               Returns:
                   List[WeatherDay]: A list of WeatherDay objects.
               """
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
    def get_average_temp_in_user_residence(cls, start_date: datetime, end_date: datetime, lat_lon: dict) -> float:
        """
                Fetch and calculate the average temperature for the user's residence for the given date range.

                Args:
                    start_date (datetime): The start date for fetching weather data.
                    end_date (datetime): The end date for fetching weather data.
                    lat_lon (dict): Latitude and longitude of the user's residence.

                Returns:
                    float: The average temperature.

                Raises:
                    ValueError: If latitude and longitude are not provided, or if no valid temperature data is found.
                """
        if not lat_lon:
            raise ValueError("Latitude and longitude must be provided")

        # Adjust the start and end months to fetch data for the previous year
        start_month = pd.Period(year=start_date.year - 1, month=start_date.month, freq='M')
        end_month = pd.Period(year=end_date.year - 1, month=end_date.month, freq='M')
        start = start_month.start_time
        end = end_month.end_time

        point = Point(lat_lon.get('lat'), lat_lon.get('lon'))

        data = Monthly(point, start, end)
        data = data.fetch()

        if 'time' in data.columns:
            data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d')

        if 'tavg' in data:
            average_temp = data['tavg']
            average_temp_list = average_temp.dropna().tolist()

            if average_temp_list:
                overall_average_temp = sum(average_temp_list) / len(average_temp_list)
                return overall_average_temp
            else:
                raise ValueError("No valid temperature data found")
        else:
            raise ValueError("No valid temperature data found")

    @classmethod
    def calculate_average_temp(cls, weather_data: List[WeatherDay]) -> float:
        """
               Calculate the average temperature from a list of WeatherDay objects.

               Args:
                   weather_data (List[WeatherDay]): List of WeatherDay objects containing daily weather information.

               Returns:
                   float: The average temperature across all provided weather days.
               """
        total_temp = 0.0
        num_days = len(weather_data)

        for day in weather_data:
            average_temp = (day.temp_max + day.temp_min) / 2
            total_temp += average_temp

        if num_days > 0:
            average_temp = total_temp / num_days
            return average_temp
        else:
            return 0.0

    @classmethod
    def check_if_raining(cls, weather_data: List[WeatherDay]) -> bool:
        """
               Determine if there is a high chance of rain based on the weather data.

               Args:
                   weather_data (List[WeatherDay]): List of WeatherDay objects containing daily weather information.

               Returns:
                   bool: True if there is a high chance of rain on any day, False otherwise.
               """
        for day in weather_data:
            if day.precip_prob > 40:
                return True
        return False

    @classmethod
    def get_user_feeling(cls, average_temp_of_trip: float,
                         users_residence_average_temp: int) -> UserWeatherFeelingOptions:
        """
              Determine how the user is likely to feel based on the average temperature of the trip compared to their
              residence's average temperature.

              Args:
                  average_temp_of_trip (float): The average temperature during the trip.
                  users_residence_average_temp (int): The average temperature of the user's residence.

              Returns:
                  UserWeatherFeelingOptions: The user's feeling about the trip's temperature (COLD, HOT, NORMAL).
              """
        if round(users_residence_average_temp) >= round(average_temp_of_trip) + 5:
            return UserWeatherFeelingOptions.COLD
        elif round(users_residence_average_temp) <= round(average_temp_of_trip - 5):
            return UserWeatherFeelingOptions.HOT
        else:
            return UserWeatherFeelingOptions.NORMAL

    @classmethod
    def adjust_temperature_based_on_feeling(cls, user_feeling: UserWeatherFeelingOptions,
                                            average_temp_of_trip: int) -> int:
        """
               Adjust the temperature in the weather data based on the user's feeling.

               Args: user_trip_average_temp (float): The average temperature of the trip. user_feeling (
               UserWeatherFeelingOptions): The user's feeling about the trip's temperature (COLD, HOT, NORMAL).

               Returns:
                   new user_trip_average_temp after the adjustment.
               """
        adjustment = 0
        if user_feeling == UserWeatherFeelingOptions.COLD:
            adjustment = -3  # decrease temperature by 3 degrees
        elif user_feeling == UserWeatherFeelingOptions.HOT:
            adjustment = 3  # increase temperature by 3 degrees
        return adjustment + average_temp_of_trip
