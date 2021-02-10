import functools
import json
import jwt
from decimal import Decimal
from tornado import web, escape


def default_encoder(obj):
    """
    JSON encoding hook to convert decimals to strings.
    """
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError


def validate_access_token(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self._validate_access_token():
            # 422 Unprocessable Entity
            # https://httpstatuses.com/422
            self.set_status(422)
            return

        return await func(self, *args, **kwargs)

    return wrapper


class BaseHandler(web.RequestHandler):
    def initialize(self, api, endpoint, http_client, jwt_secret, https_enabled=False):
        self._url = f"{api}/api/v1/{endpoint}"
        self._http_client = http_client
        self._jwt_secret = jwt_secret
        self._https_enabled = https_enabled

    async def post(self):
        """Do a post request"""
        data = json.loads(self.request.body) if self.request.body else {}
        response = await self._upsert_json_content(data, method="POST")
        return response

    async def put(self):
        """Do a put request"""
        data = json.loads(self.request.body) if self.request.body else {}
        response = await self._upsert_json_content(data, method="PUT")
        return response

    async def patch(self):
        """Do a patch request"""
        data = json.loads(self.request.body) if self.request.body else {}
        response = await self._upsert_json_content(data, method="PATCH")
        return response

    async def _upsert_json_content(self, data, method):
        """Do a request which upserts json content."""

        try:
            headers = {"Content-Type": "application/json"}

            response = await self._http_client.fetch(
                self._url,
                method=method,
                headers=headers,
                body=json.dumps(data, default=default_encoder),
            )
        except Exception as e:
            # TODO: implement logging

            http_code = e.code if hasattr(e, "code") else 500
            message = (
                e.response.body
                if hasattr(e, "response")
                else json.dumps(
                    {"message": "An error occurred, contact customer service"}
                )
            )

            self.set_status(http_code)
            self.write(message)
        else:
            self.set_status(response.code)
            self.write(escape.json_decode(response.body))
            return response

    def _create_access_token(self, response_body):
        """Creates a jwt access token based on the response body and secures it in a
        secure HTTPonly cookie.
        """
        encoded = jwt.encode(
            escape.json_decode(response_body), self._jwt_secret, algorithm="HS256"
        )
        # TODO: enable HTTPS
        # https://www.tornadoweb.org/en/stable/guide/security.html?highlight=set_secure_cookie
        self.set_secure_cookie(
            "api_access_token", encoded, secure=self._https_enabled, httponly=True
        )

    def _validate_access_token(self):
        """Validate that the user agent send the secure cookie contains the jwt access token
        which authenticates their session.
        """
        secure_cookie = self.get_secure_cookie("api_access_token")

        if not secure_cookie or not jwt.decode(
            secure_cookie, self._jwt_secret, algorithms=["HS256"]
        ):
            return False

        return True
