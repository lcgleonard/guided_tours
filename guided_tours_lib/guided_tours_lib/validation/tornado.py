import json
from functools import wraps

from voluptuous import Invalid

from .exceptions import ValidationException


def validate(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            schema = self._validator.schemas[func.__name__]
            request_method = self.request.method.lower()

            # TODO: test get request with query string
            data = (
                {k: v[0].decode() for k, v in self.request.query_arguments.items()}
                if request_method == "get"
                else json.loads(self.request.body)
            )

            validated_data = schema(data)
        except Invalid as e:
            raise ValidationException(e.error_message)
        except (AttributeError, KeyError) as e:
            raise ValidationException(e)
        return func(self, validated_data, *args, **kwargs)

    return wrapper
