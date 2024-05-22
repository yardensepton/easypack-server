from typing import List

from src.entity.item_and_calculation import ItemAndCalculation
from src.entity.packing_list import PackingList
from src.entity.packing_list_schema import PackingListSchema
from src.entity.packing_list_update import PackingListUpdate
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

    def get_packing_list_by_trip_id(self, trip_id: str) -> PackingList:
        packing_list: PackingList = self.db_handler.find_one("trip_id", trip_id)
        if packing_list:
            return packing_list

    def delete_packing_list_by_trip_id(self, trip_id: str) -> None:
        packing_list = self.get_packing_list_by_trip_id(trip_id)
        if packing_list is not None:
            self.db_handler.delete_one("trip_id", trip_id)

    def delete_packing_list_by_id(self, list_id: str) -> None:
        packing_list = self.get_packing_list_by_id(list_id)
        if packing_list is not None:
            self.db_handler.delete_one("_id", list_id)

    def get_all_packing_lists(self) -> List[PackingList]:
        return self.db_handler.find_all()

    # def remove_item(self, list_id: str, name: str) -> PackingList:
    #     remove_query = {
    #         "$pull": {"items": {"name": name}}
    #     }
    #     updated = self.db_handler.find_one_and_update(remove_query, list_id)
    #     if updated is not None:
    #         return updated
    #     raise NotFoundError(obj_name="list", obj_id=list_id)

    def add_item(self, list_id: str, details: ItemAndCalculation):
        new_info_dict = details.model_dump(by_alias=True, exclude_unset=True)
        self.db_handler.add(new_info=new_info_dict, new_info_name="items",
                            value=list_id)

    def update_item(self, list_id: str, details: ItemAndCalculation):
        new_info_dict = details.model_dump(by_alias=True, exclude_unset=True)
        self.db_handler.update_specific_field(outer_value=list_id, inner_value=details.name, inner_value_name="name",
                                              outer_value_name="items",
                                              update_fields=new_info_dict)

    def remove_item(self, list_id: str, item_name: str):
        # logging.debug(f"Removing item with id {item_id} from list {list_id}")
        self.db_handler.remove_specific_field(outer_value_name="items", inner_value_name="name",
                                              outer_value=list_id, inner_value=item_name)
