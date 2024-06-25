from pydantic import EmailStr

from src.common.common_validation import validate_non_none_fields
from src.controllers.city_controller import CityController
from src.models.auth_info import AuthInfo
from src.models.user_boundary import UserBoundary
from src.models.user_entity import UserEntity
from src.models.user_schema import UserSchema
from src.services.user_service import UserService


class UserController:

    def __init__(self):
        self.user_service = UserService()
        self.city_controller = CityController()

    def create_user(self, user: UserBoundary) -> UserEntity:
        if validate_non_none_fields(obj=user) is True:
            # user.city.currency_code = self.city_controller.get_country_code(user.city.country_name)
            return self.user_service.create_user(user)

    def get_user_by_id(self, user_id: str) -> UserEntity:
        return self.user_service.get_user_by_id(user_id)

    def get_user_by_email(self, email: EmailStr) -> UserEntity:
        return self.user_service.get_user_by_email(email)

    def delete_user_by_id(self, user_id: str):
        self.user_service.delete_user_by_id(user_id)

    def update_user_by_id(self, new_info: UserSchema, user_id: str) -> UserEntity:
        return self.user_service.update_user_by_id(new_info, user_id)

    def authenticate_user_or_abort(self, user_model: AuthInfo) -> UserEntity:
        return self.user_service.authenticate_user_or_abort(user_model)

    def user_reset_password(self, new_password: str, user: UserEntity) -> bool:
        return self.user_service.user_reset_password(new_password, user)
