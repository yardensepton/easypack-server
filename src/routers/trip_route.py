from typing import List, Optional, Union

from fastapi import APIRouter, Query, HTTPException
from starlette import status

from src.controllers import UserController
from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.entity.trip import Trip
from src.entity.update_trip import TripUpdate
from src.exceptions.input_error import InputError
from src.exceptions.trip_not_found_error import TripNotFoundError
from src.exceptions.user_not_found_error import UserNotFoundError

router = APIRouter(
    prefix="/trips",
    tags=["TRIPS"]
)

trip_controller = TripController()
packing_list_controller = PackingListController()
user_controller = UserController()

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
# Define the API key for authentication
API_KEY = ""


# Define the function to construct the URL
def construct_url(location: str, departure: str, arrival: str) -> str:
    url = f"{BASE_URL}{location}"
    if departure:
        url += f"/{departure}"
    if arrival:
        url += f"/{arrival}"
    return url


# @router.get("/{location}")
# async def get_weather(location: str, departure: str = Query(None, description="Departure date (YYYY-MM-DD)"),
#                       arrival: str = Query(None, description="Arrival date (YYYY-MM-DD)")) -> dict:
#     # Validate the departure and arrival dates if provided
#     if departure:
#         try:
#             date_parser.parse(departure)
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Invalid departure date format. Please use YYYY-MM-DD.")
#     if arrival:
#         try:
#             date_parser.parse(arrival)
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Invalid arrival date format. Please use YYYY-MM-DD.")
#
#     # Construct the URL using the location and optional dates
#     url = construct_url(location, departure, arrival)
#
#     # Define the query parameters
#     params = {
#         "unitGroup": "metric",
#         "key": API_KEY,
#         "contentType": "json"
#     }
#
#     # Use an asynchronous HTTP client to make the request
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, params=params)
#
#         # Check if the response was successful
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")
#
#         # Parse the JSON data from the response
#         weather_data = response.json()
#
#         # Return the weather data
#         return weather_data

@router.post("", response_model=Trip)
async def create_trip(trip: Trip) -> Trip:
    try:
        user_controller.get_user_by_id(trip.user_id)
        return trip_controller.create_trip(trip)
    except UserNotFoundError as unf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(unf))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except InputError as de:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(de))


@router.get("/", response_model=Union[Trip, Optional[List[Trip]]])
async def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
        user_id: Optional[str] = Query(None, description="User ID")):
    if trip_id is not None:
        try:
            return trip_controller.get_trip_by_id(trip_id)
        except TripNotFoundError as tnf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(tnf))


    elif user_id is not None:
        try:
            user_controller.get_user_by_id(user_id)
        except UserNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        trips = trip_controller.get_trips_by_user_id(user_id)
        if trips is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this user")
        return trips

        # If neither trip_id nor user_id is provided, return all trips
    else:
        trips = trip_controller.get_all_trips()
        if trips is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no trips in the DB")
        return trips


@router.delete("/{trip_id}", response_model=None)
async def delete_trip_by_id(trip_id: str):
    try:
        trip_controller.get_trip_by_id(trip_id)
        packing_list_controller.delete_packing_list_by_trip_id(trip_id)
        trip_controller.delete_trip_by_id(trip_id)
    except TripNotFoundError as tnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(tnf))


@router.put("/{trip_id}", response_model=Trip)
async def update_trip_by_id(new_info: TripUpdate, trip_id: str):
    try:
        trip_controller.get_trip_by_id(trip_id)
        return trip_controller.update_trip_by_id(new_info, trip_id)
    except TripNotFoundError as tnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(tnf))
    except InputError as ie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ie))
