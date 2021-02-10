from string import ascii_lowercase, ascii_uppercase, digits
from voluptuous import Schema, And, Coerce, Invalid, Length
from guided_tours_lib.email import is_email_address
from .helpers import special_symbols


def _validate_username(username):
    """Validate a username"""
    if len(username) != len(username.replace(" ", "")):
        raise Invalid("username should not contain any whitespace")

    return username


def _validate_email(email):
    """Validate a user's email address"""

    if not is_email_address(email):
        raise Invalid(f"Not a valid email address: {email}")

    return email


def _validate_password(pwd):
    """Validate a user's password.

    Password must contain at least 1 of each of the following:
        a lowercase letter,
        an uppercase letter,
        a number/digit,
        a special symbol
    """

    if not any(character in ascii_lowercase for character in pwd):
        raise Invalid("Password must contain at least one lowercase letter")

    if not any(character in ascii_uppercase for character in pwd):
        raise Invalid("Password must contain at least one uppercase letter")

    if not any(character in digits for character in pwd):
        raise Invalid("Password must contain at least one number")

    if not any(character in special_symbols for character in pwd):
        raise Invalid(
            f"Password must contain at least one special symbol from {special_symbols}"
        )

    return pwd


class UserValidator(object):
    """Validation class for user."""

    username = And(Coerce(str), Length(min=3, max=16), _validate_username)
    email = And(Coerce(str), Length(min=8, max=120), _validate_email)
    password = And(Coerce(str), Length(min=8, max=16), _validate_password)
    schemas = {
        "post": Schema(
            {"username": username, "email": email, "password": password}, required=True
        )
    }
