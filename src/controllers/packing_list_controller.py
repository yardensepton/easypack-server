from typing import List

from src.entity.packing_list import PackingList
from src.entity.packing_list_schema import PackingListSchema
from src.services.packing_list_service import PackingListService


class PackingListController:

    def __init__(self):
        self.packing_list_service = PackingListService()

    def create_packing_list(self, packing_list: PackingList)->PackingList:
        return self.packing_list_service.create_packing_list(packing_list=packing_list)

    def get_packing_list_by_id(self, list_id: str)->PackingList:
        return self.packing_list_service.get_packing_list_by_id(list_id=list_id)

    def get_packing_list_by_trip_id(self, trip_id: str)->PackingList:
        return self.packing_list_service.get_packing_list_by_trip_id(trip_id=trip_id)

    def delete_packing_list_by_id(self, list_id: str):
        return self.packing_list_service.delete_packing_list_by_id(list_id=list_id)

    def delete_packing_list_by_trip_id(self, trip_id: str):
        return self.packing_list_service.delete_packing_list_by_trip_id(trip_id=trip_id)

    def update_packing_list_by_id(self, new_info: PackingListSchema, list_id):
        return self.packing_list_service.update_packing_list_by_id(new_info=new_info, list_id=list_id)

    def get_all_packing_lists(self)->List[PackingList]:
        return self.packing_list_service.get_all_packing_lists()
