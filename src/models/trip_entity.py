from pydantic import Field

from src.models import PyObjectId
from src.models.trip_boundary import TripBoundary
from typing import Optional, List

from src.models.weather import WeatherDay


class TripEntity(TripBoundary):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    weather_data: Optional[List[WeatherDay]] = None
