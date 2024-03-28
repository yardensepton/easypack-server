from src.entity.packing_list import PackingList
from src.entity.trip import Trip
from src.services.packing_list_service import PackingListService
from src.services.trip_service import TripService


class PackingListTripService:
    def __init__(self):
        self.trip_service = TripService()
        self.packing_list_service = PackingListService()


    def create_list_and_add_trip(self, trip_id: str, packing_list:PackingList):
        """
        Create a packing list and associate it with the trip.
        """
        trip_dict = self.trip_service.get_trip_by_id(trip_id)
        trip = Trip(**trip_dict)
        return self.packing_list_service.create_packing_list(trip_id=trip.id,packing_list=packing_list)


    def delete_trip_and_packing_list(self, trip_id: str):
        """
        Delete trip and packing list associated.
        """
        self.packing_list_service.delete_packing_list_by_trip_id(trip_id=trip_id)
        self.trip_service.delete_trip_by_id(trip_id=trip_id)


    def get_trip_packing_list(self, trip_id: str):
        """
        Get packing list associated with trip_id.
        """
        self.trip_service.get_trip_by_id(trip_id=trip_id)
        return self.packing_list_service.get_packing_list_by_trip_id(trip_id=trip_id)

