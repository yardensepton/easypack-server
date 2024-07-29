# import unittest
# from unittest.mock import patch
#
# from src.enums.gender_options import GenderOptions
# from src.enums.role_options import RoleOptions
# from src.models.city import City
# from src.models.user_entity import UserEntity
# from src.services.user_service import UserService
# from src.utils.authantication.password_utils import get_password_hash, verify_password_hash
#
#
# class TestUserService(unittest.TestCase):
#     def setUp(self):
#         # Set up the mock for DBHandler
#         self.mock_db_handler = patch('src.services.user_service.UsersDB', autospec=True).start()
#         self.addCleanup(patch.stopall)  # Ensure patches are cleaned up after each test
#         self.user_service = UserService()
#         self.user_id = 'test_user_id'
#         self.email = 'test1@example.com'
#         self.password = '111Aa'
#         self.name = 'Test User'
#         self.gender = 'male'
#         self.city: City = City(text="tel aviv,Israel", place_id="111", city_name="tel aviv", country_name="israel")
#
#     def test_create_user_success(self) -> None:
#         self.mock_db_handler.return_value.find_one.return_value = None
#
#         # Create a sample user object
#         sample_user = UserEntity(email=self.email, name=self.name, gender=GenderOptions.MALE, city=self.city,
#                                  password=self.password, role=RoleOptions.MEMBER)
#
#         # Configure the insert_one method of the mock DBHandler instance
#         return_user=self.mock_db_handler.return_value.insert_one.return_value = {
#             'email': self.email,
#             'name': self.name,
#             'gender': self.gender,
#             'city': self.city,
#             'password': get_password_hash(self.password),
#             'role': sample_user.role
#         }
#
#         # Perform the action being tested
#         created_user = self.user_service.create_user(sample_user)
#
#         # Assertions and verification
#         self.assertEqual(created_user['email'], self.email)
#         self.assertEqual(created_user['name'], self.name)
#         self.assertEqual(created_user['gender'], self.gender)
#         self.assertEqual(created_user['city'], self.city)
#         # self.assertEqual(created_user['password'], verify_password_hash(self.password, return_user['password']))
#
#         # Verify that insert_one method of the mock DBHandler was called with the sample_user
#         self.mock_db_handler.return_value.insert_one.assert_called_once_with(sample_user)
#
#         # Verify that find_one method of the mock DBHandler was called with "email" and sample_user.email
#         self.mock_db_handler.return_value.find_one.assert_called_once_with("email", self.email)
#
#
# if __name__ == '__main__':
#     unittest.main()
import unittest
from unittest.mock import patch, MagicMock

from src.enums.gender_options import GenderOptions
from src.enums.role_options import RoleOptions
from src.models.city import City
from src.models.user_entity import UserEntity
from src.services.user_service import UserService
from src.utils.authantication.password_utils import get_password_hash, verify_password_hash


class TestUserService(unittest.TestCase):
    def setUp(self):
        # Set up the mock for DBHandler
        self.mock_db_handler_class = patch('src.services.user_service.UsersDB', autospec=True).start()
        self.mock_db_handler = self.mock_db_handler_class.return_value
        self.addCleanup(patch.stopall)  # Ensure patches are cleaned up after each test
        self.user_service = UserService()
        self.user_id = 'test_user_id'
        self.email = 'test1@example.com'
        self.password = '111Aa'
        self.name = 'Test User'
        self.gender = GenderOptions.MALE
        self.city: City = City(text="tel aviv,Israel", place_id="111", city_name="tel aviv", country_name="israel")

    def test_create_user_success(self) -> None:
        self.mock_db_handler.find_one.return_value = None

        # Create a sample user object
        sample_user = UserEntity(email=self.email, name=self.name, gender=self.gender, city=self.city,
                                 password=self.password, role=RoleOptions.MEMBER, id=None)

        # Configure the insert_one method of the mock DBHandler instance
        hashed_password = get_password_hash(self.password)
        inserted_user = UserEntity(
            email=self.email,
            name=self.name,
            gender=self.gender,
            city=self.city,
            password=hashed_password,
            role=RoleOptions.MEMBER,
            id=self.user_id  # This will be set by MongoDB
        )

        self.mock_db_handler.insert_one.return_value = inserted_user

        # Perform the action being tested
        created_user = self.user_service.create_user(sample_user)

        # Assertions and verification
        self.assertEqual(created_user.id, self.user_id)
        self.assertEqual(created_user.email, self.email)
        self.assertEqual(created_user.name, self.name)
        self.assertEqual(created_user.gender, self.gender)
        self.assertEqual(created_user.city, self.city)
        self.assertEqual(created_user.password, hashed_password)  # Check hashed password

        # Verify that insert_one method of the mock DBHandler was called with the correct user entity
        self.mock_db_handler.insert_one.assert_called_once()
        inserted_user_call = self.mock_db_handler.insert_one.call_args[0][0]

        # Compare fields except the password
        self.assertEqual(inserted_user_call.email, self.email)
        self.assertEqual(inserted_user_call.name, self.name)
        self.assertEqual(inserted_user_call.gender, self.gender)
        self.assertEqual(inserted_user_call.city, self.city)
        self.assertEqual(inserted_user_call.role, RoleOptions.MEMBER)
        self.assertIsNone(inserted_user_call.id)  # ID should be None when calling insert_one

        # Verify that find_one method of the mock DBHandler was called with "email" and sample_user.email
        self.mock_db_handler.find_one.assert_called_once_with("email", self.email)


if __name__ == '__main__':
    unittest.main()
