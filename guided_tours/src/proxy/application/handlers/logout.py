import json
from .base import BaseHandler, validate_access_token


class LogoutHandler(BaseHandler):
    @validate_access_token
    async def post(self):
        """Do a post request"""

        data = json.loads(self.request.body) if self.request.body else {}

        response = await self._upsert_json_content(data, method="POST")

        self.clear_cookie("api_access_token")

        return response
