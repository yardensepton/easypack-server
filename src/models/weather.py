from typing import Dict

from pydantic import BaseModel


class WeatherDay(BaseModel):
    datetime: str
    temp_max: float
    temp_min: float
    feels_like: float
    precip_prob: float
    wind_speed: float
    conditions: str
    icon: str

    def to_dict(self) -> Dict:
        return {
            'datetime': self.datetime,
            'temp_max': self.temp_max,
            'temp_min': self.temp_min,
            'feels_like': self.feels_like,
            'precip_prob': self.precip_prob,
            'wind_speed': self.wind_speed,
            'conditions': self.conditions,
            'icon': self.icon,
        }
