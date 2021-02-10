from decimal import Decimal
from voluptuous import Schema, And, Coerce, Length, Invalid, Optional
from .helpers import special_symbols
from .user import UserValidator


def _validate_search_string(search_string):
    """Validate a search string."""

    if any(character in special_symbols for character in search_string):
        raise Invalid(
            f"Search string must not contain any special symbols from {special_symbols}"
        )

    return search_string


def _validate_title(title):
    """Validate the title of the tour."""

    if any(character in special_symbols for character in title):
        raise Invalid(
            f"title must not contain any special symbols from {special_symbols}"
        )

    return title


class ToursValidator(object):
    """Validation class for tour details."""

    tour_id = Coerce(int)
    title = And(Coerce(str), Length(min=3, max=50), _validate_title)
    description = And(Coerce(str), Length(min=5, max=255))
    latitude = Coerce(Decimal)
    longitude = Coerce(Decimal)

    key = And(Coerce(str), Length(min=5, max=50))
    filename = And(Coerce(str), Length(min=5, max=120))
    content_type = And(Coerce(str), Length(min=5, max=25))
    extension = And(Coerce(str), Length(min=3, max=10))

    upsert_schema = Schema(
        {
            "username": UserValidator.username,
            "title": title,
            "description": description,
            "latitude": latitude,
            "longitude": longitude,
        },
        required=True,
    )

    schemas = {
        "get": Schema(
            {
                Optional("username"): UserValidator.username,
                Optional("latitude"): latitude,
                Optional("longitude"): longitude,
            }
        ),
        "post": upsert_schema,
        "put": upsert_schema,
        "patch": Schema(
            [
                Schema(
                    {
                        "key": key,
                        "name": filename,
                        "content_type": content_type,
                        "extension": extension,
                    },
                    required=True,
                )
            ]
        ),
    }
