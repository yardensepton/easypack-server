from src.entity.user import User
from src.services.user_service import UserService


class UserController:

    def __init__(self):
        self.user_service = UserService()

    def create_user(self, user: User):
        return self.user_service.create_user(user)

    def get_user_by_id(self, user_id):
        return self.user_service.get_user_by_id(user_id)


    def delete_user_by_id(self, user_id):
        self.user_service.delete_user_by_id(user_id)

    def update_user_by_id(self, new_info, user_id):
        return self.user_service.update_user_by_id(new_info, user_id)