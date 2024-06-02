from typing import List

from src.models.item_and_calculation import ItemAndCalculation
from src.models.packing_list_entity import PackingListEntity
from src.models.packing_list_boundary import PackingListBoundary
from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.not_found_error import NotFoundError
from db import db
from src.repositories.packing_lists_db import PackingListsDB


class PackingListService:
    def __init__(self):
        self.db_handler = PackingListsDB(db, "LISTS")

    def get_packing_list_by_id(self, list_id: str) -> PackingListEntity:
        packing_list = self.db_handler.find_one("_id", list_id)
        if packing_list is not None:
            return packing_list
        raise NotFoundError(obj_name="Packing list", obj_id=list_id)

    def create_packing_list(self, trip_id: str, packing_list: PackingListBoundary) -> PackingListEntity:
        if self.get_packing_list_by_trip_id(trip_id):
            raise AlreadyExistsError(obj_name="packing list to trip", obj_id=trip_id)
        packing_list_entity: PackingListEntity = PackingListEntity(trip_id=trip_id, items=packing_list.items)
        return self.db_handler.insert_one(packing_list_entity)

    def get_packing_list_by_trip_id(self, trip_id: str) -> PackingListEntity:
        packing_list: PackingListEntity = self.db_handler.find_one("trip_id", trip_id)
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

    def get_all_packing_lists(self) -> List[PackingListEntity]:
        return self.db_handler.find_all()

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
