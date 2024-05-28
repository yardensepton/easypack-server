from pydantic import BaseModel
from typing import List


class WeatherDay(BaseModel):
    datetime: str
    temp_max: float
    temp_min: float
    feels_like: float
    precip_prob: float
    wind_speed: float
    conditions: str
    icon: str
