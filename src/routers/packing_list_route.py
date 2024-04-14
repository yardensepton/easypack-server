from typing import List, Optional, Union

from fastapi import APIRouter, Query


from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.entity.packing_list import PackingList


router = APIRouter(
    prefix="/packing-lists",
    tags=["PACKING_LISTS"]
)


list_controller = PackingListController()
trip_controller = TripController()

@router.post("/", response_model=PackingList)
def create_packing_list(packing_list: PackingList) -> PackingList:
    trip_controller.get_trip_by_id(packing_list.trip_id)
    return list_controller.create_packing_list(packing_list)


@router.get("/", response_model=Union[PackingList, Optional[List[PackingList]]])
def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
              list_id: Optional[str] = Query(None, description="List ID")):
    if trip_id is not None:
        # If trip_id is provided, return the packing list with that trip ID
       trip_controller.get_trip_by_id(trip_id)
       return list_controller.get_packing_list_by_trip_id(trip_id)
    elif list_id is not None:
        # If list_id is provided, return the list with that list ID
       return list_controller.get_packing_list_by_id(list_id)



@router.delete("/{list_id}", response_model=None)
def delete_packing_list_by_id(list_id: str):
    list_controller.delete_packing_list_by_id(list_id)


# @router.put("/{list_id}", response_model=Trip)
# def update_packing_list_by_id(new_info: ListUpdate, list_id: str):
#     return list_controller.update_packing_list_by_id(new_info, list_id)
