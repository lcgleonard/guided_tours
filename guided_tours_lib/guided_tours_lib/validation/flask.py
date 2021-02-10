from functools import wraps
from flask import request
from voluptuous import Invalid
from .exceptions import ValidationException


def validate(func):
    """Validation decorator.

    Example usage:
        class MyResourceValidator:
            schema = {
                "post": <Validation Schema Object>
            }

        class MyResource:
            @validate
            def post(self, data): ...
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            # get the validation schema for this method
            schema = self._validator.schemas[func.__name__]

            # get the data from the request.  If request is POST then get JSON (only JSON
            # is allowed - no XML or Text)
            data = (
                request.args.to_dict()
                if request.method == "GET"
                else request.get_json()
            )

            # validate the data against the schema
            data = schema(data)
        except Invalid as e:
            print(e)  # TODO: implement logging
            raise ValidationException(e.error_message)
        except (AttributeError, KeyError) as ve:
            print(ve)  # TODO: implement logging
            raise ValidationException(e)

        # call function with validated data
        return func(self, data, *args, **kwargs)

    return wrapper
