from src.services.item_service import ItemService
from src.services.packing_list_service import PackingListService


class PackingListController:

    def __init__(self):
        self.packing_list_service = PackingListService()
        self.item_service = ItemService()

    def create_packing_list(self, packing_list):
        return self.packing_list_service.create_packing_list(packing_list)

    def get_packing_list_by_id(self, list_id):
        return self.packing_list_service.get_packing_list_by_id(list_id)

    def get_packing_list_by_trip_id(self, trip_id):
        return self.packing_list_service.get_packing_list_by_trip_id(trip_id)

    def delete_packing_list_by_id(self, list_id):
        return self.packing_list_service.delete_packing_list_by_id(list_id)

    def delete_packing_list_by_trip_id(self,trip_id):
        return self.packing_list_service.delete_packing_list_by_trip_id(trip_id=trip_id)
