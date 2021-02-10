import asyncio
import json
import logging
import uuid
from http import HTTPStatus

import aioredis
from tornado import web, escape, websocket


logger = logging.getLogger("tornado.access")


# Borg Pattern
# "Just about every application need related to Singleton is met by ensuring that
# all instances share state and behavior, which is easier and more flexible than
# fiddling with instance creation." Ref:
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s23.html
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class RedisBorg(Borg):
    pool = None

    @classmethod
    async def initialize(cls, redis_host, loop):
        cls.pool = await aioredis.create_pool(
            redis_host, minsize=5, maxsize=10, loop=loop
        )

    @classmethod
    async def execute(cls, *args, **kwargs):
        return await cls.pool.execute(*args, **kwargs)


class WsClients(Borg):
    clients = {}

    @classmethod
    def add(cls, client, data):
        cls.clients[client] = data

    @classmethod
    def remove(cls, client):
        del cls.clients[client]


class TokenCache(Borg):
    @staticmethod
    async def add(token, value):
        """Add a token as a key with its value to redis"""
        await RedisBorg().execute("SET", token, value)
        ttl = 5000
        return await RedisBorg().execute("EXPIRE", token, ttl)

    @staticmethod
    async def get(token):
        """Add a token value from redis"""
        return await RedisBorg().execute("GET", token)

    @staticmethod
    async def remove(token):
        """Remove a token value from redis"""
        return await RedisBorg().execute("DEL", token)


class WebSocketHandler(websocket.WebSocketHandler):
    _token_cache = TokenCache()
    _ws_client_store = WsClients()

    def check_origin(self, origin):
        # Due to time pressures I haven't implemented CORS but
        # I am using token authentication.  I would enables CORS
        # and each the token authentication as an extra layer of
        # security
        # TODO: enable CORS
        return True

    def open(self):
        logger.info(f"Opening ws client {self} connection")

    async def on_message(self, message):
        parsed_msg = escape.json_decode(message)

        if parsed_msg["action"] == "register":
            cache_token = await self._token_cache.get(parsed_msg["token"])

            if cache_token:
                self._ws_client_store.add(
                    self,
                    {
                        "latitude": parsed_msg["latitude"],
                        "longitude": parsed_msg["longitude"],
                    },
                )
                logger.info(f"Adding ws client {self}")
                await self._token_cache.remove(parsed_msg["token"])

    def on_close(self):
        if self in self._ws_client_store.clients:
            self._ws_client_store.remove(self)
            logger.info(f"Removing ws client {self}")


class WebSocketTokenHandler(web.RequestHandler):
    _token_cache = TokenCache()

    async def get(self):
        token = str(uuid.uuid1())

        await self._token_cache.add(token, str(self))

        self.set_status(HTTPStatus.CREATED)
        self.write(json.dumps({"token": token}))
