from typing import List, Optional, Union


from fastapi import APIRouter, Query

from src.controllers import UserController
from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.entity.trip import Trip
from src.entity.update_trip import TripUpdate


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
def create_trip(trip: Trip) -> Trip:
    user_controller.get_user_by_id(trip.user_id)
    return trip_controller.create_trip(trip)


@router.get("/", response_model=Union[Trip, Optional[List[Trip]]])
def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
              user_id: Optional[str] = Query(None, description="User ID")):
    if trip_id is not None:
        # If trip_id is provided, return the trip with that ID
       return trip_controller.get_trip_by_id(trip_id)
    elif user_id is not None:
        # If user_id is provided, return trips by user_id
       return trip_controller.get_trips_by_user_id_with_exception(user_id)
    else:
        return trip_controller.get_all_trips()

@router.delete("/{trip_id}", response_model=None)
def delete_trip_by_id(trip_id: str):
    packing_list_controller.delete_packing_list_by_trip_id(trip_id)
    trip_controller.delete_trip_by_id(trip_id)


@router.put("/{trip_id}", response_model=Trip)
def update_trip_by_id(new_info: TripUpdate, trip_id: str):
    return trip_controller.update_trip_by_id(new_info, trip_id)
