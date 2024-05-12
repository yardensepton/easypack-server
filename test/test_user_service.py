import unittest
from unittest.mock import patch
from src.entity.user import User
from src.services.user_service import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        # Set up the mock for DBHandler
        self.mock_db_handler = patch('src.services.user_service.db_handler.DBHandler', autospec=True).start()
        self.addCleanup(patch.stopall)  # Ensure patches are cleaned up after each test
        self.user_service = UserService()
        self.user_id = 'test_user_id'
        self.email = 'test1@example.com'
        self.name = 'Test User'
        self.gender = 'male'
        self.residence = 'Test Residence'

    def test_create_user_success(self) -> None:
        self.mock_db_handler.return_value.find_one.return_value = None

        # Create a sample user object
        sample_user = User(email=self.email, name=self.name, gender=self.gender, residence=self.residence, id=self.user_id)

        # Configure the insert_one method of the mock DBHandler instance
        self.mock_db_handler.return_value.insert_one.return_value = {
            '_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'gender': self.gender,
            'residence': self.residence
        }

        # Perform the action being tested
        created_user = self.user_service.create_user(sample_user)

        # Assertions and verification
        self.assertEqual(created_user['_id'], self.user_id)
        self.assertEqual(created_user['email'], self.email)
        self.assertEqual(created_user['name'], self.name)
        self.assertEqual(created_user['gender'], self.gender)
        self.assertEqual(created_user['residence'], self.residence)

        # Verify that insert_one method of the mock DBHandler was called with the sample_user
        self.mock_db_handler.return_value.insert_one.assert_called_once_with(sample_user)

        # Verify that find_one method of the mock DBHandler was called with "email" and sample_user.email
        self.mock_db_handler.return_value.find_one.assert_called_once_with("email", self.email)


if __name__ == '__main__':
    unittest.main()
