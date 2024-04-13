from src.entity.trip import Trip
from src.services.trip_service import TripService
from src.services.user_service import UserService


class TripUserService:
    def __init__(self):
        self.trip_service = TripService()
        self.user_service = UserService()

    def delete_user_and_trips(self, user_id: str):
        """
        Delete user and all trips associated.
        """
        self.trip_service.delete_trips_by_user_id(user_id=user_id)
        self.user_service.delete_user_by_id(user_id=user_id)


    def create_trip_and_add_user(self,trip:Trip):
        """
        Create a trip and associate it with the user.
        """
        user = self.user_service.get_user_by_id(trip.user_id)
        return self.trip_service.create_trip(user_id=trip.user_id,trip=trip,user=user)


    def get_user_trips(self, user_id: str):
        """
        Delete user and all trips associated.
        """
        self.user_service.get_user_by_id(user_id=user_id)
        return self.trip_service.get_trips_by_user_id_with_exception(user_id=user_id)