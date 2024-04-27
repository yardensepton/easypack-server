from typing import List, Optional, Union

from fastapi import APIRouter, Query, HTTPException
from starlette import status

from src.controllers.item_controller import ItemController
from src.controllers.packing_list_controller import PackingListController
from src.controllers.trip_controller import TripController
from src.entity.packing_list import PackingList
from src.exceptions.packing_list_already_exists_error import PackingListAlreadyExistsError
from src.exceptions.packing_list_not_found_error import PackingListNotFoundError
from src.exceptions.trip_not_found_error import TripNotFoundError

router = APIRouter(
    prefix="/packing-lists",
    tags=["PACKING_LISTS"]
)

list_controller = PackingListController()
trip_controller = TripController()


@router.post("/", response_model=PackingList)
async def create_packing_list(packing_list: PackingList) -> PackingList:
    try:
        trip_controller.get_trip_by_id(packing_list.trip_id)
        return list_controller.create_packing_list(packing_list)
    except TripNotFoundError as tnf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(tnf))
    except PackingListAlreadyExistsError as pae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(pae))


@router.get("/", response_model=Union[PackingList, Optional[List[PackingList]]])
async def get(trip_id: Optional[str] = Query(None, description="Trip ID"),
              list_id: Optional[str] = Query(None, description="List ID")):
    if list_id is not None:
        try:
            return list_controller.get_packing_list_by_id(list_id)
        except PackingListNotFoundError as pnf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(pnf))


    elif trip_id is not None:
        try:
            trip_controller.get_trip_by_id(trip_id)
            packing_list = list_controller.get_packing_list_by_trip_id(trip_id)
            if packing_list is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Trip {trip_id} doesn't have a packing list")
        except TripNotFoundError as tnf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(tnf))


@router.delete("/{list_id}", response_model=None)
async def delete_packing_list_by_id(list_id: str):
    try:
        list_controller.get_packing_list_by_id(list_id)
        list_controller.delete_packing_list_by_id(list_id)
    except PackingListNotFoundError as pnf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(pnf))

# @router.put("/{list_id}", response_model=Trip)
# def update_packing_list_by_id(new_info: ListUpdate, list_id: str):
#     return list_controller.update_packing_list_by_id(new_info, list_id)
