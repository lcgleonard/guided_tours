import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus

from tornado import escape

from guided_tours_lib.validation.tours import ToursValidator
from guided_tours_lib.validation.tornado import validate

from ..lib.content import get_file_path, get_file_name
from ..lib.threadpool import run_in_threadpool, remove_content_from_disk
from .base import BaseHandler, validate_access_token, default_encoder
from .web_socket import WsClients

logger = logging.getLogger("tornado.access")


class ToursHandler(BaseHandler):
    _ws_client_store = WsClients()
    _validator = ToursValidator

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

    def _upload_files(self, tour_id):
        files_uploaded = []
        files_not_uploaded = []

        for key, file_data in self.request.files.items():
            # file data is awkwardly a list containing a single element
            # which is the dict containing the uploaded audio or img data
            _file_data = file_data[0]

            filename = _file_data["filename"]
            binary_content = _file_data["body"]
            content_type = _file_data["content_type"]
            extension = os.path.splitext(filename)[1]

            server_file_path = get_file_path(self._base_content_path, key)

            server_filename = get_file_name(tour_id, content_type, filename, extension)

            server_file_location = f"{server_file_path}{server_filename}"

            data = {
                "key": key,
                "name": filename,
                "content_type": content_type,
                "extension": extension,
            }

            try:
                exists = os.path.isfile(server_file_location)

                if exists:
                    # if the file already exists, then skip the saving of it
                    files_not_uploaded.append(data)
                    continue
            except Exception:
                files_not_uploaded.append(data)
                logger.error(str(e))
                continue

            with open(server_file_location, "wb") as _file:
                try:
                    _file.write(binary_content)
                except Exception as e:
                    logger.error(str(e))
                    files_not_uploaded.append(data)
                else:
                    files_uploaded.append(data)

        return files_uploaded, files_not_uploaded

    async def _upload_files_threadpool_wrapper(self, tour_id, loop):
        # I'm running the method _upload_files inside asyncio's thread pool
        # executor because it performs a blocking io action which writes
        # the files to disk
        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, self._upload_files, tour_id)

    @validate_access_token
    async def patch(self, tour_id):
        """Do a patch request"""

        try:

            files_uploaded, files_not_uploaded = await run_in_threadpool(
                self._upload_files, tour_id
            )
        except Exception as e:
            logger.error(f"Error when writing files to disk: {e}")
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            self._url = self._url.format(tour_id)

            response = await self._upsert_json_content(files_uploaded, method="PATCH")

            return response

    @validate
    async def get(self, data, *args, **kwargs):
        """Get a tour by it's id or tours by a query string."""

        if args and args[0].isdigit():
            tour_id = int(args[0])
            self._url = self._url.format(tour_id)
        elif "username" in data:
            params = f"?username={data['username']}"
            self._url = self._url.format(params)
        elif "latitude" in data and "longitude" in data:
            params = f"?latitude={data['latitude']}&longitude={data['longitude']}"
            self._url = self._url.format(params)
        else:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"message": "Bad Request"})
            return

        response = await self._http_client.fetch(self._url, method="GET")

        response_body = escape.json_decode(response.body)

        if "content" in response_body:
            for content in response_body["content"]:
                content["server_filename"] = get_file_name(
                    response_body["tour_id"],
                    content["content_type"],
                    content["name"],
                    content["extension"],
                )

        self.set_status(response.code)
        self.write(response_body)
        return response

    @validate_access_token
    @validate
    async def post(self, data, *args, **kwargs):
        """Do a post request"""

        self._url = self._url.format("")

        logger.debug(f"POST for {self._url} with data {data}")

        title = data["title"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        response = await self._http_client.fetch(
            self._url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(data, default=default_encoder),
        )

        if response is None:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        if response.code == HTTPStatus.CREATED:
            response_body = json.loads(response.body)

            for client, data in self._ws_client_store.clients.items():
                # TODO: check if this client should be subscribed for this tour
                # based on latitude and longitude

                client.write_message(
                    json.dumps(
                        {
                            "action": "tour_added",
                            "tour": {
                                "tour_id": response_body["tour_id"],
                                "title": title,
                                "latitude": latitude,
                                "longitude": longitude,
                            },
                        },
                        default=default_encoder,
                    )
                )

            self.set_status(response.code)
            self.write(response_body)

        return response

    @validate_access_token
    @validate
    async def put(self, data, tour_id):
        """Do a put request"""

        self._url = self._url.format(tour_id)

        logger.debug(f"PUT for {self._url} with data {data}")

        title = data["title"]
        latitude = data["latitude"]
        longitude = data["longitude"]

        response = await self._http_client.fetch(
            self._url,
            method="PUT",
            headers={"Content-Type": "application/json"},
            body=json.dumps(data, default=default_encoder),
        )

        if response.code == HTTPStatus.OK:
            # TODO: check if this client was subscribed for this tour
            for client, data in self._ws_client_store.clients.items():
                client.write_message(
                    json.dumps(
                        {
                            "action": "tour_updated",
                            "tour": {
                                "tour_id": tour_id,
                                "title": title,
                                "latitude": latitude,
                                "longitude": longitude,
                            },
                        },
                        default=default_encoder,
                    )
                )
            self.set_status(response.code)
            self.write(escape.json_decode(response.body))

        return response

    @validate_access_token
    async def delete(self, tour_id):
        """Do a delete request"""

        self._url = self._url.format(tour_id)

        response = await self._http_client.fetch(self._url, method="DELETE")

        if response.code == HTTPStatus.OK:
            response_body = escape.json_decode(response.body)

            tasks = []

            for data in response_body["tour"]["content"]:
                server_file_path = get_file_path(self._base_content_path, data["key"])

                server_filename = get_file_name(
                    tour_id, data["content_type"], data["name"], data["extension"]
                )

                server_file_location = f"{server_file_path}{server_filename}"
                tasks.append(remove_content_from_disk(server_file_location))

            if tasks:
                await asyncio.gather(*tasks)

            for client, data in self._ws_client_store.clients.items():
                # TODO: check if this client was subscribed for this tour
                client.write_message(
                    json.dumps({"action": "tour_deleted", "tour_id": tour_id})
                )

        self.set_status(response.code)

        return response
