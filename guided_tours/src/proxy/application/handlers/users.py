import json
from guided_tours_lib.validation.user import UserValidator
from guided_tours_lib.validation.tornado import validate
from .base import BaseHandler, validate_access_token


class UserHandler(BaseHandler):
    _validator = UserValidator

    @validate
    async def post(self, data, *args, **kwargs):
        """Do a post request"""
        self._url = self._url.format("")
        response = await self._upsert_json_content(data, method="POST")

        if response.code == 201:
            self._create_access_token(response.body)

        return response

    @validate_access_token
    async def put(self, username):
        """Do a put request"""

        self._url = self._url.format(username)
        data = json.loads(self.request.body) if self.request.body else {}
        response = await self._upsert_json_content(data, method="PUT")

        # I'm clearing the api_access_token cookie regardless of the response
        # from the api as a security precaution
        self.clear_cookie("api_access_token")

        return response

    @validate_access_token
    async def patch(self, username):
        """Do a patch request"""

        self._url = self._url.format(username)
        data = json.loads(self.request.body) if self.request.body else {}
        response = await self._upsert_json_content(data, method="PATCH")

        # I'm clearing the api_access_token cookie regardless of the response
        # from the api as a security precaution
        self.clear_cookie("api_access_token")

        return response
