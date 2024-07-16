from typing import List, Optional, Union

from fastapi import APIRouter, Query, HTTPException, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.controllers import UserController
from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.models.trip_boundary import TripBoundary
from src.models.trip_entity import TripEntity
from src.models.trip_info import TripInfo
from src.models.trip_update import TripUpdate
from src.models.user_entity import UserEntity
from src.enums.role_options import RoleOptions
from src.models.weather import WeatherDay
from src.utils.authantication.current_identity_utils import get_current_access_identity
from src.utils.decorators.relationship_decorator import user_trip_access_or_abort
from src.utils.decorators.user_decorator import user_permission_check
from src.routers.weather_route import get_weather

router = APIRouter(
    prefix="/trips",
    tags=["TRIPS"]
)

trip_controller = TripController()
packing_list_controller = PackingListController()
user_controller = UserController()


@router.post("", response_model=TripEntity)
async def create_trip(trip: TripBoundary, identity: UserEntity = Depends(get_current_access_identity)):
    trip_entity: TripEntity = TripEntity(departure_date=trip.departure_date, return_date=trip.return_date,
                                         user_id=identity.id, destination=trip.destination)
    if trip_controller.availability_within_date_range(identity.id, trip.departure_date, trip.return_date,
                                                      trip_entity.id):
        weather_data: List[WeatherDay] = await get_weather(trip_entity.destination.city_name,
                                                           trip_entity.departure_date,
                                                           trip_entity.return_date)
        trip_entity.weather_data = weather_data
        trip_entity_in_db: TripEntity = trip_controller.create_trip(trip_entity)

        return JSONResponse(status_code=status.HTTP_200_OK, content=trip_entity_in_db.dict())


@router.get("", response_model=Union[TripEntity, Optional[List[TripEntity]]])
async def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
              user_id: Optional[str] = Query(None, description="User ID"),
              identity: UserEntity = Depends(get_current_access_identity)):
    if trip_id is not None:
        trip = await get_trip_by_id(trip_id=trip_id, identity=identity)
        return JSONResponse(status_code=status.HTTP_200_OK, content=trip.dict())

    elif user_id is not None:
        trips: List[TripEntity] = await get_trips_by_user_id(user_id=user_id, identity=identity)
        return JSONResponse(status_code=status.HTTP_200_OK, content=[trip.dict() for trip in trips])

    else:
        if identity.role == RoleOptions.ADMIN.value:
            trips = trip_controller.get_all_trips()
            if trips is None or len(trips) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no trips in the DB")
            # return trips
            return JSONResponse(status_code=status.HTTP_200_OK, content=[trip.dict() for trip in trips])
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="permission denied")


@user_trip_access_or_abort
async def get_trip_by_id(trip_id: str, identity: UserEntity) -> TripEntity:
    return trip_controller.get_trip_by_id(trip_id)


@user_permission_check
async def get_trips_by_user_id(user_id: str, identity: UserEntity):
    user_controller.get_user_by_id(user_id)
    trips = trip_controller.get_trips_by_user_id(user_id)
    if trips is None or len(trips) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this user")
    return JSONResponse(status_code=status.HTTP_200_OK, content=[trip.dict() for trip in trips])


@router.get("/sorted", response_model=Union[TripInfo, Optional[List[TripInfo]]])
async def get_sorted_trips_info_by_current_user(identity: UserEntity = Depends(get_current_access_identity)):
    user_controller.get_user_by_id(identity.id)
    trips: List[TripInfo] = trip_controller.get_sorted_trips_info(identity.id)
    print(f"trips len is {len(trips)} ")
    return JSONResponse(status_code=status.HTTP_200_OK, content=[trip.dict() for trip in trips])


@router.get("/upcoming-trip", response_model=TripEntity)
async def get_users_upcoming_trip(identity: UserEntity = Depends(get_current_access_identity),
                                  ):
    user_controller.get_user_by_id(identity.id)
    upcoming_trip: TripEntity = trip_controller.get_users_upcoming_trip(identity.id)
    if upcoming_trip is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this user")
    return JSONResponse(status_code=status.HTTP_200_OK, content=upcoming_trip.dict())


@router.delete("/{trip_id}", response_model=None)
@user_trip_access_or_abort
async def delete_trip_by_id(trip_id: str, identity: UserEntity = Depends(get_current_access_identity)):
    packing_list_controller.get_packing_list_by_trip_id(trip_id)
    packing_list_controller.delete_packing_list_by_trip_id(trip_id)
    trip_controller.delete_trip_by_id(trip_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"Trip {trip_id} deleted")


@router.put("/{trip_id}", response_model=TripEntity)
@user_trip_access_or_abort
async def update_trip_by_id(new_info: TripUpdate, trip_id: str,
                            identity: UserEntity = Depends(get_current_access_identity)):
    updated_trip: TripEntity = trip_controller.update_trip_by_id(new_info, trip_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_trip.dict())
