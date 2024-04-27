from src.controllers.packing_list_controller import PackingListController
from src.entity.trip import Trip
from src.services.trip_service import TripService


class TripController:

    def __init__(self):
        self.trip_service = TripService()
        self.packing_list_controller = PackingListController()

    def create_trip(self, trip):
        return self.trip_service.create_trip(trip)

    def get_trip_by_id(self, trip_id):
        return self.trip_service.get_trip_by_id(trip_id)

    def get_trips_by_user_id(self, user_id):
        return self.trip_service.get_trips_by_user_id(user_id)

    def delete_trip_by_id(self, trip_id):
        self.trip_service.delete_trip_by_id(trip_id)

    def delete_trips_by_user_id(self, user_id):
        trips = self.get_trips_by_user_id(user_id)
        if trips is not None:
            for trip_data in trips:
                trip = Trip(**trip_data)
                trip_id = trip.id

                if trip_id is not None:
                    self.packing_list_controller.delete_packing_list_by_trip_id(trip_id)
                    self.delete_trip_by_id(trip_id)

    def update_trip_by_id(self, new_info, trip_id):
        return self.trip_service.update_trip_by_id(new_info, trip_id)

    def get_all_trips(self):
        return self.trip_service.get_all_trips()
