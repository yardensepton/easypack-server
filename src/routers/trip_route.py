from typing import List, Optional, Union

from fastapi import APIRouter, Query, HTTPException
from starlette import status

from src.controllers import UserController
from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.entity.trip import Trip
from src.entity.trip_schema import TripSchema

router = APIRouter(
    prefix="/trips",
    tags=["TRIPS"]
)

trip_controller = TripController()
packing_list_controller = PackingListController()
user_controller = UserController()


@router.post("", response_model=Trip)
async def create_trip(trip: Trip) -> Trip:
    user_controller.get_user_by_id(trip.user_id)
    return trip_controller.create_trip(trip)


@router.get("", response_model=Union[Trip, Optional[List[Trip]]])
async def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
              user_id: Optional[str] = Query(None, description="User ID")):
    if trip_id is not None:
        return trip_controller.get_trip_by_id(trip_id)
    elif user_id is not None:
        user_controller.get_user_by_id(user_id)
        trips = trip_controller.get_trips_by_user_id(user_id)
        if trips is None or len(trips) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this user")
        return trips
        # If neither trip_id nor user_id is provided, return all trips
    else:
        trips = trip_controller.get_all_trips()
        if trips is None or len(trips) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no trips in the DB")
        return trips


@router.delete("/{trip_id}", response_model=None)
async def delete_trip_by_id(trip_id: str):
    trip_controller.get_trip_by_id(trip_id)
    packing_list_controller.delete_packing_list_by_trip_id(trip_id)
    trip_controller.delete_trip_by_id(trip_id)


@router.put("/{trip_id}", response_model=Trip)
async def update_trip_by_id(new_info: TripSchema, trip_id: str):
    trip_controller.get_trip_by_id(trip_id)
    return trip_controller.update_trip_by_id(new_info, trip_id)
