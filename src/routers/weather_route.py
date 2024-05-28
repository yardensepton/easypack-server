import os
from typing import List

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Query, HTTPException

from src.controllers.weather_controller import WeatherController
from src.entity.weather import WeatherDay

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
    # Construct the URL using the location and optional dates
    url = construct_url(location, departure, arrival)
    load_dotenv()
    weather_api_key = os.getenv("WEATHER_API_KEY")

    # Define the query parameters
    params = {
        "unitGroup": "metric",
        "key": weather_api_key,
        "contentType": "json",
        "include": "days"
    }
    weather_controller.get_average_weather()

    # Use an asynchronous HTTP client to make the request
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        # Check if the response was successful
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")

        # Parse the JSON data from the response
        weather_data = response.json()

        # Return the weather data
        return weather_controller.create_weather_objects(weather_data)
