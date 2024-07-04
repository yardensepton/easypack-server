from typing import List

from src.models.packing_list_boundary import PackingListBoundary
from src.models.packing_list_entity import PackingListEntity
from src.models.packing_list_update import PackingListUpdate
from src.enums.operation import Operation
from src.models.trip_entity import TripEntity
from src.models.user_entity import UserEntity
from src.services.packing_list_service import PackingListService


class PackingListController:

    def __init__(self):
        self.packing_list_service = PackingListService()

    def create_packing_list(self, trip: TripEntity,
                            user: UserEntity, lat_lon: dict) -> PackingListEntity:
        return self.packing_list_service.create_packing_list(trip=trip, user=user,
                                                             lat_lon=lat_lon)

    def get_packing_list_by_id(self, list_id: str) -> PackingListEntity:
        return self.packing_list_service.get_packing_list_by_id(list_id=list_id)

    def get_packing_list_by_trip_id(self, trip_id: str) -> PackingListEntity:
        return self.packing_list_service.get_packing_list_by_trip_id(trip_id=trip_id)

    def delete_packing_list_by_id(self, list_id: str):
        return self.packing_list_service.delete_packing_list_by_id(list_id=list_id)

    def delete_packing_list_by_trip_id(self, trip_id: str):
        return self.packing_list_service.delete_packing_list_by_trip_id(trip_id=trip_id)

    def update_packing_list_by_id(self, new_info: List[PackingListUpdate], list_id) -> PackingListEntity:
        for update in new_info:
            if update.operation == Operation.update:
                self.packing_list_service.update_item(list_id, update.details)
            elif update.operation == Operation.remove:
                self.packing_list_service.remove_item(list_id, update.details.name)
            elif update.operation == Operation.add:
                self.packing_list_service.add_item(list_id=list_id, details=update.details)
        return self.packing_list_service.get_packing_list_by_id(list_id)

    def get_all_packing_lists(self) -> List[PackingListEntity]:
        return self.packing_list_service.get_all_packing_lists()
