import logging
import re
from fastapi import HTTPException
from starlette import status

from db import db
from src.entity.user import User
from src.exceptions.input_error import InputError
from src.exceptions.user_already_exists_error import UserAlreadyExistsError
from src.exceptions.user_not_found_error import UserNotFoundError
from src.repositories import db_handler


class UserService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "USERS")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    def create_user(self, user: User):
        if self.check_user(user.email) and self.is_valid_email_format(user.email):
            return self.db_handler.insert_one(user)

    def check_user(self, email: str):
        if self.db_handler.find_one("email", email) is not None:
            raise UserAlreadyExistsError(email)
        return True

    def is_valid_email_format(self, email):
        email_regex = r"(^[-!#$%&'*+/=?^_`{|}~a-zA-Z0-9]+(\.[-\w]*)*@[-a-zA-Z0-9]+(\.[-\w]*)+\.?[a-zA-Z]{2,}$)"
        if bool(re.match(email_regex, email)) is False:
            raise InputError("Invalid email format")
        return True

    def get_user_by_id(self, user_id: str):
        user = self.db_handler.find_one("_id", user_id)
        if user is not None:
            return user
        raise UserNotFoundError(user_id)

    def delete_user_by_id(self, user_id):
        user = self.db_handler.find_one("_id", user_id)
        if user is not None:
            self.db_handler.delete_one("_id", user_id)

    def update_user_by_id(self, new_info, user_id):
        # adding the input values to a dict if they are not null
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }
        # updating the user with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, user_id)
        if updated is not None:
            return updated
        raise UserNotFoundError(user_id)
