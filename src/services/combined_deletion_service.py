from src.entity.trip import Trip
from src.services.packing_list_trip_service import PackingListTripService
from src.services.trip_user_service import TripUserService
from src.services.user_service import UserService


class CombinedDeletionService:
    def __init__(self):
        self.trip_user_service = TripUserService()
        self.packing_list_trip_service = PackingListTripService()
        self.user_service = UserService()

    def delete_user_and_associated_data(self, user_id):
        # Delete all trips associated with the user
        trips_deleted = self.trip_user_service.get_user_trips(user_id)
        trips_deleted_casted = [Trip(**trip_data) for trip_data in trips_deleted]

        print(trips_deleted_casted)
        # Iterate over the deleted trips and delete their associated packing lists
        for trip in trips_deleted_casted:
            self.packing_list_trip_service.delete_trip_and_packing_list(trip.id)

        # Delete the user
        self.user_service.delete_user_by_id(user_id)
