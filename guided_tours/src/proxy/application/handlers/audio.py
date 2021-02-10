from http import HTTPStatus

from tornado import escape


from ..lib.content import get_file_name, get_file_path
from ..lib.threadpool import remove_content_from_disk
from .base import BaseHandler, validate_access_token


class AudioHandler(BaseHandler):
    def initialize(
        self,
        api,
        endpoint,
        http_client,
        jwt_secret,
        https_enabled=False,
        base_content_path="",
    ):
        self._url = f"{api}/api/v1/{endpoint}"
        self._http_client = http_client
        self._jwt_secret = jwt_secret
        self._https_enabled = https_enabled
        self._base_content_path = base_content_path

    @validate_access_token
    async def delete(self, tour_id):
        """Do a delete request"""

        self._url = self._url.format(tour_id)
        response = await self._http_client.fetch(self._url, method="DELETE")

        if response.code == 200:
            data = escape.json_decode(response.body)
            server_file_path = get_file_path(self._base_content_path, data["key"])

            server_filename = get_file_name(
                tour_id, data["content_type"], data["name"], data["extension"]
            )

            server_file_location = f"{server_file_path}{server_filename}"

            try:
                await remove_content_from_disk(server_file_location)
            except OSError:
                self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.write({"message": "Server Error"})
                return

        return response
