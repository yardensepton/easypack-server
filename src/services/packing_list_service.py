from fastapi import HTTPException
from starlette import status
from src.repositories import db_handler
from db import db


class PackingListService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "LISTS")

    def get_packing_list_by_id(self, list_id):
        packing_list = self.db_handler.find_one("_id", list_id)
        if packing_list is not None:
            return packing_list
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List {list_id} not found")

    def create_packing_list(self, packing_list):
        if self.check_trip_has_packing_list(packing_list.trip_id) is False:
            return self.db_handler.insert_one(packing_list)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"There is already a packing list to trip {packing_list.trip_id}")

    def check_trip_has_packing_list(self, trip_id) -> bool:
        packing_list = self.get_packing_list_by_trip_id(trip_id)
        if isinstance(packing_list, str):
            # there is already packing list associated with the trip
            return True
        elif packing_list is None:
            return False

    def get_packing_list_by_trip_id(self, trip_id):
        packing_list = self.db_handler.find({"trip_id": trip_id})
        if len(packing_list) != 0:
            return packing_list
        return None

    def delete_packing_list_by_trip_id(self, trip_id):
        packing_list = self.get_packing_list_by_trip_id(trip_id)
        if packing_list is not None:
            self.db_handler.delete_many({"trip_id": trip_id})

    def delete_packing_list_by_id(self, list_id):
        packing_list = self.get_packing_list_by_id(list_id)
        if packing_list is not None:
            self.db_handler.delete_one("_id", list_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"packing list {list_id} not found")
