from typing import List

import httpx

from fastapi import APIRouter, Query, HTTPException

from config import WEATHER_API_KEY
from src.controllers.weather_controller import WeatherController
from src.models.weather import WeatherDay

router = APIRouter(
    prefix="/weather",
    tags=["WEATHER"]
)

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

weather_controller = WeatherController()


def construct_url(location: str, departure: str, arrival: str) -> str:
    url = f"{BASE_URL}{location}"
    if departure:
        url += f"/{departure}"
    if arrival:
        url += f"/{arrival}"
    return url


@router.get("")
async def get_weather(location: str, departure: str = Query(None, description="Departure date (YYYY-MM-DD)"),
                      arrival: str = Query(None, description="Arrival date (YYYY-MM-DD)")) -> List[WeatherDay]:
    url = construct_url(location, departure, arrival)

    params = {
        "unitGroup": "metric",
        "key": WEATHER_API_KEY,
        "contentType": "json",
        "include": "days"
    }
    weather_controller.get_average_weather()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")

        weather_data = response.json()
        print(weather_data)

        return weather_controller.create_weather_objects(weather_data)
