from voluptuous import Schema, Optional, And, Invalid
from .user import UserValidator


def _validate_username_or_email_supplied(data):
    if "username" not in data:
        if "email" not in data:
            raise Invalid("No username or email supplied for login.")

    return data


class UserLoginValidator(object):
    """Validation class for user login."""

    schemas = {
        "post": And(
            Schema(
                {
                    Optional("username"): UserValidator.username,
                    Optional("email"): UserValidator.email,
                    "password": UserValidator.password,
                },
                required=True,
            ),
            _validate_username_or_email_supplied,
        )
    }
