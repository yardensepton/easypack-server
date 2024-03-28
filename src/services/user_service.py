import logging

from fastapi import HTTPException
from starlette import status

from db import db
from src.entity.user import User
from src.repositories import  db_handler


class UserService:
    def __init__(self):
        self.db_handler = db_handler.DBHandler(db, "USERS")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log',
                        filemode='w')

    def create_user(self, user: User):
        self.check_user(user.email)
        return self.db_handler.insert_one(user)

    def check_user(self, email: str):
        if self.db_handler.find_one("email", email) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"user with email {email} already exists")

    def get_user_by_email(self, email: str):
        user = self.db_handler.find_one("email", email)
        if user is not None:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with email {email} not found")

    def get_user_by_id(self, user_id: str):
        user = self.db_handler.find_one("_id", user_id)
        if user is not None:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user_id} not found")


    def delete_user_by_id(self, user_id):
        user = self.db_handler.find_one("_id", user_id)
        if user is not None:
            self.db_handler.delete_one("_id", user_id)
            logging.info(f"deleted user : {user_id}")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user_id} not found")

    def update_user_by_id(self, new_info, user_id):
        # adding the input values to a dict if they are not null
        new_info_dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }
        # updating the user with the new info
        updated = self.db_handler.find_one_and_update(new_info_dict, user_id)
        if updated is not None:
            return updated
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user_id} not found")
