from typing import List

from src.models.packing_list_entity import PackingListEntity
from src.models.packing_list_request import PackingListRequest
from src.models.packing_list_update import PackingListUpdate
from src.enums.action import Action
from src.models.trip_entity import TripEntity
from src.models.user_entity import UserEntity
from src.services.packing_list_service import PackingListService


class PackingListController:

    def __init__(self):
        self.packing_list_service = PackingListService()

    async def create_packing_list(self, trip: TripEntity,
                                  user: UserEntity, lat_lon: dict,
                                  packing_list_request: PackingListRequest) -> PackingListEntity:
        return await self.packing_list_service.create_packing_list(trip=trip, user=user,
                                                                   packing_list_request=packing_list_request,
                                                                   lat_lon=lat_lon)

    def get_packing_list_by_id(self, list_id: str) -> PackingListEntity:
        return self.packing_list_service.get_packing_list_by_id(list_id=list_id)

    def get_packing_list_by_trip_id(self, trip_id: str) -> PackingListEntity:
        return self.packing_list_service.get_packing_list_by_trip_id(trip_id=trip_id)

    def delete_packing_list_by_id(self, list_id: str):
        return self.packing_list_service.delete_packing_list_by_id(list_id=list_id)

    def delete_packing_list_by_trip_id(self, trip_id: str):
        return self.packing_list_service.delete_packing_list_by_trip_id(trip_id=trip_id)

    async def update_packing_list_by_id(self, new_info: PackingListUpdate, list_id) -> PackingListEntity:
        """
        Updates a packing list based on the provided new information.

        Args:
            new_info (PackingListUpdate): An object containing details about the update action.
            list_id: The ID of the packing list to be updated.

        Returns:
            PackingListEntity: The updated packing list entity.
        """
        # Convert the category and item_name to lowercase and reassign them
        new_info.details.category = new_info.details.category.lower()
        new_info.details.item_name = new_info.details.item_name.lower()

        if new_info.action == Action.update:
            await self.packing_list_service.update_item(list_id, new_info.details)
        elif new_info.action == Action.remove:
            await self.packing_list_service.remove_item(list_id, new_info.details.item_name)
        elif new_info.action == Action.add:
            await self.packing_list_service.add_item(list_id=list_id, details=new_info.details)
        return self.packing_list_service.get_packing_list_by_id(list_id)

    def get_all_packing_lists(self) -> List[PackingListEntity]:
        return self.packing_list_service.get_all_packing_lists()
