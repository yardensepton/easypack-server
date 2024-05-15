from typing import List

from src.entity.packing_list import PackingList
from src.entity.packing_list_schema import PackingListSchema
from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.not_found_error import NotFoundError
from db import db
from src.repositories.packing_lists_db import PackingListsDB


class PackingListService:
    def __init__(self):
        self.db_handler = PackingListsDB(db, "LISTS")

    def get_packing_list_by_id(self, list_id: str) -> PackingList:
        packing_list = self.db_handler.find_one("_id", list_id)
        if packing_list is not None:
            return packing_list
        raise NotFoundError(obj_name="Packing list", obj_id=list_id)

    def create_packing_list(self, packing_list: PackingList) -> PackingList:
        if self.get_packing_list_by_trip_id(packing_list.trip_id):
            raise AlreadyExistsError(obj_name="packing list to trip", obj_id=packing_list.trip_id)
        return self.db_handler.insert_one(packing_list)

    # def check_trip_has_packing_list(self, trip_id: str) -> bool:
    #     packing_list = self.get_packing_list_by_trip_id(trip_id)
    #     if isinstance(packing_list, str):
    #         # there is already packing list associated with the trip
    #         return True
    #     elif packing_list is None:
    #         return False

    def get_packing_list_by_trip_id(self, trip_id: str) -> PackingList:
        packing_list: PackingList = self.db_handler.find_one("trip_id", trip_id)
        if packing_list:
            return packing_list

    def delete_packing_list_by_trip_id(self, trip_id: str)->None:
        packing_list = self.get_packing_list_by_trip_id(trip_id)
        if packing_list is not None:
            self.db_handler.delete_one("trip_id", trip_id)

    def delete_packing_list_by_id(self, list_id: str)->None:
        packing_list = self.get_packing_list_by_id(list_id)
        if packing_list is not None:
            self.db_handler.delete_one("_id", list_id)

    def update_packing_list_by_id(self, new_info: PackingListSchema, list_id: str)->PackingList:
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }

        # updating the user with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, list_id)
        if updated is not None:
            return updated
        raise NotFoundError(obj_name="list", obj_id=list_id)

    def get_all_packing_lists(self)-> List[PackingList]:
        return self.db_handler.find_all()
