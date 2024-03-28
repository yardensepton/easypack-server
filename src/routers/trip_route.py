from typing import List, Optional

import httpx
from fastapi import APIRouter, Query, HTTPException

from src.controllers.trip_controller import TripController
from src.entity.trip import Trip
from src.entity.update_trip import TripUpdate


router = APIRouter(
    prefix="/trips",
    tags=["TRIPS"]
)

trip_controller = TripController()
API_KEY = "37dc14380f18978f0613562bd06a2775"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@router.get("/weather")
async def get_weather(city: str, country: str):
    params = {
        "q": f"{city},{country}",
        "APPID": API_KEY,
        "units": "metric"  # Optional: specify units, e.g., metric or imperial
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")
        weather_data = response.json()
        return weather_data

@router.post("", response_model=Trip)
def create_trip(trip: Trip, user_id: str = Query(..., alias="user_id")) -> Trip:
    return trip_controller.create_trip(trip, user_id)


@router.get("/{trip_id}", response_model=Trip)
def get_trip_by_id(trip_id: str):
    return trip_controller.get_trip_by_id(trip_id)


@router.get("", response_model=Optional[List[Trip]])
def get_trips_by_user_id(user_id: str = Query(..., alias="user_id")):
    return trip_controller.get_trips_by_user_id(user_id)


@router.delete("/delete", response_model=None)
def delete_trip_by_id(trip_id: str = Query(..., alias="user_id")):
    trip_controller.delete_trip_by_id(trip_id)


@router.put("/{trip_id}", response_model=Trip)
def update_trip_by_id(new_info: TripUpdate, trip_id: str):
    return trip_controller.update_trip_by_id(new_info, trip_id)
