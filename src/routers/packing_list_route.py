from typing import List, Optional

from fastapi import APIRouter, Query

from src.controllers import UserController
from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.entity.packing_list import PackingList
from src.entity.trip import Trip
from src.entity.update_trip import TripUpdate
from src.entity.update_user import UserUpdate
from src.entity.user import User

router = APIRouter(
    prefix="/packing-lists",
    tags=["PACKING_LISTS"]
)


list_controller = PackingListController()

@router.post("", response_model=PackingList)
def create_packing_list(packing_list: PackingList, trip_id: str = Query(..., alias="trip_id")) -> PackingList:
    return list_controller.create_packing_list(packing_list ,trip_id)

@router.get("/{list_id}", response_model=PackingList)
def get_packing_list_by_id(list_id: str):
    return list_controller.get_packing_list_by_id(list_id)


@router.get("", response_model=Optional[List[PackingList]])
def get_packing_list_by_trip_id(trip_id: str = Query(..., alias="trip_id")):
    return list_controller.get_packing_list_by_trip_id(trip_id)


@router.delete("/delete", response_model=None)
def delete_packing_list_by_id(list_id: str = Query(..., alias="list_id")):
    list_controller.delete_packing_list_by_id(list_id)


# @router.put("/{list_id}", response_model=Trip)
# def update_packing_list_by_id(new_info: ListUpdate, list_id: str):
#     return list_controller.update_packing_list_by_id(new_info, list_id)
