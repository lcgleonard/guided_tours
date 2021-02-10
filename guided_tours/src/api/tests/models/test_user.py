from unittest import TestCase
from application.models.user import UserModel


class TestUserModel(TestCase):
    def test_generate_hash(self):
        password = "Test_password3*"
        hashed_password = UserModel.generate_hash(password)
        expected_hash_lenght = 87
        self.assertEqual(expected_hash_lenght, len(hashed_password))

    def test_verify_hash(self):
        password = "Test_password5*"
        hashed_password = UserModel.generate_hash(password)
        self.assertTrue(UserModel.verify_hash(password, hashed_password))
