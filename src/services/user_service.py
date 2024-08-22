from typing import Dict

from pydantic import EmailStr
from logger import logger

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
        self.logger = logger

    def create_user(self, user: UserBoundary) -> UserEntity:
        """
               Create a new user in the database if the user does not already exist.

               Args:
                   user (UserBoundary): The user details to be added.

               Returns:
                   UserEntity: The created user entity.

               Raises:
                   AlreadyExistsError: If a user with the same email already exists.
               """
        if self.check_user(user.email):
            user_to_db: UserEntity = UserEntity(name=user.name, email=user.email, city=user.city, gender=user.gender,
                                                role=user.role,
                                                password=get_password_hash(user.password))

            user_in_db: UserEntity = self.db_handler.insert_one(user_to_db)
            self.logger.info(f"User {user_in_db.id} was added successfully")
            return user_in_db

    def check_user(self, email: str) -> bool:
        """
               Check if a user with the given email already exists in the database.

               Args:
                   email (str): The email address to check.

               Returns:
                   bool: True if the user does not exist, otherwise False.

               Raises:
                   AlreadyExistsError: If a user with the same email already exists.
               """
        if self.db_handler.find_one("email", email) is not None:
            self.logger.warning(f"User with email {email} already exists")
            raise AlreadyExistsError("user", email)
        return True

    async def get_user_by_id(self, user_id: str) -> UserEntity:
        """
               Retrieve a user from the database by user ID.

               Args:
                   user_id (str): The ID of the user to retrieve.

               Returns:
                   UserEntity: The user entity if found.

               Raises:
                   NotFoundError: If no user is found with the given ID.
               """
        user: UserEntity = self.db_handler.find_one("_id", user_id)
        if user is not None:
            return user
        raise NotFoundError(obj_name="user", obj_id=user_id)

    def get_user_by_email(self, email: EmailStr) -> UserEntity:
        """
        Retrieve a user from the database by email address.

        Args:
            email (EmailStr): The email address of the user to retrieve.

        Returns:
            UserEntity: The user entity if found.
        """
        user: UserEntity = self.db_handler.find_one("email", email)
        if user is not None:
            return user

    def delete_user_by_id(self, user_id: str) -> None:
        """
               Delete a user from the database by user ID.

               Args:
                   user_id (str): The ID of the user to delete.

               Returns:
                   None
               """
        user: UserEntity = self.db_handler.find_one("_id", user_id)
        if user is not None:
            self.logger.info(f"User {user_id} was deleted")
            self.db_handler.delete_one("_id", user_id)

    def update_user_by_id(self, new_info: UserUpdate, user_id: str) -> UserEntity:
        """
        Update a user's information in the database.

        Args:
            new_info (UserUpdate): The new user information to update.
            user_id (str): The ID of the user to update.

        Returns:
            UserEntity: The updated user entity.

        Raises:
            NotFoundError: If no user is found with the given ID.
        """
        # adding the input values to a dict if they are not null
        new_info_dict: Dict = {
            k: v for k, v in new_info.model_dump(by_alias=True).items() if v is not None
        }

        # updating the user with the new info
        updated: UserEntity = self.db_handler.find_one_and_update(new_info_dict, user_id)
        if updated is not None:
            self.logger.info(f"User {user_id} updated information: {new_info_dict}")
            return updated
        raise NotFoundError(obj_name="user", obj_id=user_id)

    def authenticate_user_or_abort(self, user_model: AuthInfo) -> UserEntity:
        """
        Authenticate a user based on the provided authentication information.

        Args:
            user_model (AuthInfo): The authentication information containing username and password.

        Returns:
            UserEntity: The authenticated user entity.

        Raises:
            NotFoundError: If no user is found with the provided username.
            AuthorizationError: If the provided password does not match.
        """
        user = self.get_user_by_email(user_model.username)
        if user is None:
            self.logger.warning(f"Authentication failed: User with username {user_model.username} not found.")
            raise NotFoundError(obj_name="user", obj_id=user_model.username)
        if not verify_password_hash(given_password=user_model.password, password_hash=user.password):
            self.logger.warning(f"Authentication failed: Incorrect password for user {user_model.username}.")
            raise AuthorizationError(obj_name="user", obj_id=user_model.username)
        self.logger.info(f"Authentication succeeded: User {user_model.username} was authenticated.")
        return user

    def user_reset_password(self, new_password: str, user: UserEntity) -> bool:
        """
                Reset the password for a user.

                Args:
                    new_password (str): The new password to set.
                    user (UserEntity): The user entity for which the password is to be reset.

                Returns:
                    bool: True if the password was successfully changed, False otherwise.
                """
        if user is not None:
            user.password = get_password_hash(new_password)
            self.db_handler.find_one_and_update(user.dict(), user.id)
            self.logger.info(f"Password for user {user.id} changed successfully.")
            return True
        return False
