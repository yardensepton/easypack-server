from typing import List, Optional, Union

from fastapi import APIRouter, Query, HTTPException, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.models.packing_list_entity import PackingListEntity
from src.models.packing_list_update import PackingListUpdate
from src.models.trip_entity import TripEntity
from src.models.user_entity import UserEntity
from src.utils.authantication.current_identity_utils import get_current_access_identity
from src.utils.decorators.relationship_decorator import user_trip_access_or_abort
from src.routers.city_route import get_lat_lon

router = APIRouter(
    prefix="/packing-lists",
    tags=["PACKING_LISTS"]
)

packing_list_controller = PackingListController()
trip_controller = TripController()


@router.post("/{trip_id}", response_model=PackingListEntity)
@user_trip_access_or_abort
async def create_packing_list(trip_id: str, items_preferences: Optional[List[str]] = None,
                              activities_preferences: Optional[List[str]] = None,
                              identity: UserEntity = Depends(get_current_access_identity)):
    trip: TripEntity = trip_controller.get_trip_by_id(trip_id)
    lat_lon: dict = await get_lat_lon(trip.destination.text)
    pack_list: PackingListEntity = await packing_list_controller.create_packing_list(trip=trip,
                                                                                     user=identity, lat_lon=lat_lon,
                                                                                     activities_preferences=activities_preferences,
                                                                                     items_preferences=items_preferences)
    return JSONResponse(status_code=status.HTTP_200_OK, content=pack_list.dict())


@router.get("", response_model=Union[PackingListEntity, Optional[List[PackingListEntity]]])
async def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
              list_id: Optional[str] = Query(None, description="List ID"),
              identity: UserEntity = Depends(get_current_access_identity)):
    if list_id is not None:
        packing_list: PackingListEntity = packing_list_controller.get_packing_list_by_id(list_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=packing_list.dict())

    elif trip_id is not None:
        trip_controller.get_trip_by_id(trip_id)
        packing_list: PackingListEntity = packing_list_controller.get_packing_list_by_trip_id(trip_id)
        if packing_list is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Trip {trip_id} doesn't have a packing list")
        return JSONResponse(status_code=status.HTTP_200_OK, content=packing_list.dict())
    else:
        packing_lists: List[PackingListEntity] = packing_list_controller.get_all_packing_lists()
        if len(packing_lists) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no packing lists in the DB")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=[packing_list.dict() for packing_list in packing_lists])


@router.delete("/{trip_id}/{list_id}", response_model=None)
@user_trip_access_or_abort
async def delete_packing_list_by_id(trip_id: str, list_id: str,
                                    identity: UserEntity = Depends(get_current_access_identity)):
    packing_list_controller.delete_packing_list_by_id(list_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"Packing list {list_id} deleted")


@router.put("/{trip_id}/{list_id}", response_model=PackingListEntity)
@user_trip_access_or_abort
async def update_packing_list_by_id(new_info: List[PackingListUpdate], list_id: str, trip_id: str,
                                    identity: UserEntity = Depends(get_current_access_identity)):
    print(list_id)
    updated_packing_list: PackingListEntity = await packing_list_controller.update_packing_list_by_id(new_info, list_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_packing_list.dict())
