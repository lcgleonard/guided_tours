import json
from .base import BaseHandler


class LoginHandler(BaseHandler):
    async def post(self):
        """Do a post request"""
        data = json.loads(self.request.body) if self.request.body else {}
        response = await self._upsert_json_content(data, method="POST")

        if response.code == 200:
            self._create_access_token(response.body)

        return response
