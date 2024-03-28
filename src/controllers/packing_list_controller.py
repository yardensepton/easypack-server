from src.services.packing_list_service import PackingListService
from src.services.packing_list_trip_service import PackingListTripService


class PackingListController:

    def __init__(self):
        self.packing_list_service = PackingListService()
        self.packing_list_trip_service = PackingListTripService()


    def create_packing_list(self, packing_list, trip_id):
        return self.packing_list_trip_service.create_list_and_add_trip(trip_id, packing_list)

    def get_packing_list_by_id(self, list_id):
        return self.packing_list_service.get_packing_list_by_id(list_id)

    def get_packing_list_by_trip_id(self, trip_id):
        return self.packing_list_trip_service.get_trip_packing_list(trip_id)

    def delete_packing_list_by_id(self, list_id):
        return self.packing_list_service.delete_packing_list_by_id(list_id)
