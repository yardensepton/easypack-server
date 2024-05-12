import logging

from db import db
from src.entity.user import User
from src.entity.user_schema import UserSchema
from src.exceptions.already_exists_error import AlreadyExistsError
from src.exceptions.not_found_error import NotFoundError
from src.repositories import db_handler


class UserService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "USERS")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    def create_user(self, user: User) -> User:
        if self.check_user(user.email):
            return self.db_handler.insert_one(user)

    def check_user(self, email: str) -> bool:
        if self.db_handler.find_one("email", email) is not None:
            raise AlreadyExistsError("user", email)
        return True

    def get_user_by_id(self, user_id: str) -> User:
        user = self.db_handler.find_one("_id", user_id)
        if user is not None:
            return user
        raise NotFoundError(obj_name="user", obj_id=user_id)

    def delete_user_by_id(self, user_id: str):
        user = self.db_handler.find_one("_id", user_id)
        if user is not None:
            self.db_handler.delete_one("_id", user_id)

    def update_user_by_id(self, new_info: UserSchema, user_id: str) -> User:
        # adding the input values to a dict if they are not null
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }

        # updating the user with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, user_id)
        if updated is not None:
            return updated
        raise NotFoundError(obj_name="user", obj_id=user_id)
