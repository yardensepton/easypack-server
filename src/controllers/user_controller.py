from src.entity.user import User
from src.services.combined_deletion_service import CombinedDeletionService
from src.services.trip_user_service import TripUserService
from src.services.user_service import UserService


class UserController:

    def __init__(self):
        self.user_service = UserService()
        self.trip_user_service = TripUserService()
        self.combined_deletion_service = CombinedDeletionService()

    def create_user(self, user: User):
        return self.user_service.create_user(user)

    def get_user_by_id(self, user_id):
        return self.user_service.get_user_by_id(user_id)

    def get_user_by_email(self, user_email):
        return self.user_service.get_user_by_email(user_email)

    def delete_user_by_id(self, user_id):
        self.combined_deletion_service.delete_user_and_associated_data(user_id)

    def update_user_by_id(self, new_info, user_id):
        return self.user_service.update_user_by_id(new_info, user_id)