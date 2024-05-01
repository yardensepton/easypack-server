from typing import List, Optional, Union

from fastapi import APIRouter, Query, HTTPException
from starlette import status

from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.entity.packing_list import PackingList
from src.entity.packing_list_schema import PackingListSchema

router = APIRouter(
    prefix="/packing-lists",
    tags=["PACKING_LISTS"]
)

list_controller = PackingListController()
trip_controller = TripController()


@router.post("/", response_model=PackingList)
async def create_packing_list(packing_list: PackingList):
    trip_controller.get_trip_by_id(packing_list.trip_id)
    return list_controller.create_packing_list(packing_list)


@router.get("/", response_model=Union[PackingList, Optional[List[PackingList]]])
async def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
              list_id: Optional[str] = Query(None, description="List ID")):
    if list_id is not None:
        return list_controller.get_packing_list_by_id(list_id)

    elif trip_id is not None:
        trip_controller.get_trip_by_id(trip_id)
        packing_list = list_controller.get_packing_list_by_trip_id(trip_id)
        if packing_list is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Trip {trip_id} doesn't have a packing list")
        return packing_list
    else:
        packing_lists = list_controller.get_all_packing_lists()
        if len(packing_lists) ==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no packing lists in the DB")
        return packing_lists


@router.delete("/{list_id}", response_model=None)
async def delete_packing_list_by_id(list_id: str):
    list_controller.get_packing_list_by_id(list_id)
    list_controller.delete_packing_list_by_id(list_id)

@router.put("/{list_id}", response_model=PackingList)
def update_packing_list_by_id(new_info:PackingListSchema , list_id: str):
    return list_controller.update_packing_list_by_id(new_info, list_id)
