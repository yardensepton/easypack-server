from src.services.packing_list_trip_service import PackingListTripService
from src.services.trip_service import TripService
from src.services.trip_user_service import TripUserService


class TripController:

    def __init__(self):
        self.trip_service = TripService()
        self.trip_user_service = TripUserService()
        self.packing_list_trip_service = PackingListTripService()

    def create_trip(self, trip, user_id):
        return self.trip_user_service.create_trip_and_add_user(user_id, trip)

    def get_trip_by_id(self, trip_id):
        return self.trip_service.get_trip_by_id(trip_id)

    def get_trips_by_user_id(self, user_id):
        return self.trip_service.get_trips_by_user_id_with_exception(user_id)

    def delete_trip_by_id(self, trip_id):
        self.packing_list_trip_service.delete_trip_and_packing_list(trip_id)

    def update_trip_by_id(self, new_info, trip_id):
        return self.trip_service.update_trip_by_id(new_info, trip_id)
