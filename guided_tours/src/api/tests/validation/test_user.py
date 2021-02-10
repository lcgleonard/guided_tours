from unittest import TestCase
from application.lib.validation.user import (
    UserValidator,
    _validate_username,
    _validate_email,
    _validate_password,
    Invalid,
)


class TestUserValidation(TestCase):
    def test_validate_username_is_valid(self):
        username = "test_user"
        self.assertEqual(username, _validate_username(username))

    def test_validate_username_is_not_valid(self):
        with self.assertRaises(Invalid):
            r = _validate_username("test with spaces")
            print(r)

    def test_validate_email_is_valid(self):
        email = "lorcan@gmail.com"
        self.assertEqual(email, _validate_email(email))

    def test_validate_email_is_not_valid(self):
        with self.assertRaises(Invalid):
            _validate_email("lorcan_at_gmail.com")

    def test_validate_password_is_valid(self):
        password = "Just right !1"
        self.assertTrue(password, _validate_password(password))

    def test_validate_password_is_not_valid_no_uppercase_letters(self):
        with self.assertRaises(Invalid):
            _validate_password("no uppercase!1")

    def test_validate_password_is_not_valid_no_lowercase_letters(self):
        with self.assertRaises(Invalid):
            _validate_password("NO LOWER CASE!1")

    def test_validate_password_is_not_valid_no_numbers(self):
        with self.assertRaises(Invalid):
            _validate_password("No numbers!")

    def test_validate_password_is_not_valid_no_special_characters(self):
        with self.assertRaises(Invalid):
            _validate_password("No special chars1")

    def test_user_validation_post_schema_is_valid(self):
        data = {
            "username": "test_user",
            "email": "lorcan@gmail.com",
            "password": "Just right !1",
        }
        schema = UserValidator.schemas["post"]
        self.assertDictEqual(data, schema(data))

    def test_user_validation_post_schema_is_not_valid_email(self):
        data = {
            "username": "test_user",
            "email": "lorcan_at_gmail.com",
            "password": "Just right !1",
        }
        schema = UserValidator.schemas["post"]

        with self.assertRaises(Invalid):
            schema(data)

    def test_user_validation_post_schema_is_not_valid_username_too_short(self):
        data = {"username": "te", "email": "lorcan@gmail.com", "password": "2_short"}
        schema = UserValidator.schemas["post"]

        with self.assertRaises(Invalid):
            schema(data)

    def test_user_validation_post_schema_is_not_valid_username_too_long(self):
        data = {
            "username": "test_username_is_too_long_and_should_be_rejected_by_the_validation",
            "email": "lorcan@gmail.com",
            "password": "Just right !1",
        }
        schema = UserValidator.schemas["post"]

        with self.assertRaises(Invalid):
            schema(data)

    def test_user_validation_post_schema_is_not_valid_password_too_long(self):
        data = {
            "username": "test_user",
            "email": "lorcan@gmail.com",
            "password": "This password is too long and should be rejected by the validation!1",
        }
        schema = UserValidator.schemas["post"]

        with self.assertRaises(Invalid):
            schema(data)
