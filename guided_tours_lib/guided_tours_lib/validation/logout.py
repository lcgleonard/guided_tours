from voluptuous import Schema
from .user import UserValidator


class UserLogoutValidator(object):
    """Validation class for user logout."""

    schemas = {"post": Schema({"username": UserValidator.username}, required=True)}
