import logging
from typing import Dict

from pydantic import EmailStr


from db import db
from src.models.auth_info import AuthInfo
from src.models.user_boundary import UserBoundary
from src.models.user_entity import UserEntity
from src.models.user_update import UserUpdate
from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.authorization_error import AuthorizationError
from src.exceptions.not_found_error import NotFoundError
from src.repositories.users_db import UsersDB
from src.utils.authantication.password_utils import get_password_hash, verify_password_hash


class UserService:
    def __init__(self):
        self.db_handler = UsersDB(db, "USERS")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    def create_user(self, user: UserBoundary) -> UserEntity:
        if self.check_user(user.email):
            user_in_db: UserEntity = UserEntity(name=user.name, email=user.email, city=user.city, gender=user.gender,
                                                role=user.role,
                                                password=get_password_hash(user.password))

            return self.db_handler.insert_one(user_in_db)

    def check_user(self, email: str) -> bool:
        if self.db_handler.find_one("email", email) is not None:
            raise AlreadyExistsError("user", email)
        return True

    async def get_user_by_id(self, user_id: str) -> UserEntity:
        user: UserEntity = self.db_handler.find_one("_id", user_id)
        if user is not None:
            return user
        raise NotFoundError(obj_name="user", obj_id=user_id)

    def get_user_by_email(self, email: EmailStr) -> UserEntity:
        user: UserEntity = self.db_handler.find_one("email", email)
        if user is not None:
            return user

    def delete_user_by_id(self, user_id: str) -> None:
        user: UserEntity = self.db_handler.find_one("_id", user_id)
        if user is not None:
            self.db_handler.delete_one("_id", user_id)

    def update_user_by_id(self, new_info: UserUpdate, user_id: str) -> UserEntity:
        # adding the input values to a dict if they are not null
        new_info_dict: Dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }

        # updating the user with the new info
        updated: UserEntity = self.db_handler.find_one_and_update(new_info_dict, user_id)
        if updated is not None:
            return updated
        raise NotFoundError(obj_name="user", obj_id=user_id)

    def authenticate_user_or_abort(self, user_model: AuthInfo) -> UserEntity:
        user = self.get_user_by_email(user_model.username)
        if user is None:
            raise NotFoundError(obj_name="user", obj_id=user_model.username)
        if not verify_password_hash(given_password=user_model.password, password_hash=user.password):
            raise AuthorizationError(obj_name="user", obj_id=user_model.username)
        return user

    def user_reset_password(self, new_password: str, user: UserEntity) -> bool:
        if user is not None:
            user.password = get_password_hash(new_password)
            self.db_handler.find_one_and_update(user.dict(), user.id)
            return True
        return False
