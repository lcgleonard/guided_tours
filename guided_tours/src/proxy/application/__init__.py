import logging
import sys

import tornado.log
import tornado.web
from tornado import httpclient

from .handlers import (
    UserHandler,
    AudioHandler,
    ImagesHandler,
    LoginHandler,
    LogoutHandler,
    ToursHandler,
    WebSocketHandler,
    TokenCache,
    WebSocketTokenHandler,
    WsClients,
    RedisBorg,
)


async def init_borgs(options_, loop):
    WsClients()
    TokenCache()
    await RedisBorg().initialize(options_.redis_host, loop)


def make_app(options_):
    return tornado.web.Application(
        [
            (
                r"/api/v1/login",
                LoginHandler,
                dict(
                    api=options_.api_host,
                    endpoint="login",
                    http_client=httpclient.AsyncHTTPClient(),
                    jwt_secret=options_.jwt_secret,
                    https_enabled=options_.https_enabled,
                ),
            ),
            (
                r"/api/v1/logout",
                LogoutHandler,
                dict(
                    api=options_.api_host,
                    endpoint="logout",
                    http_client=httpclient.AsyncHTTPClient(),
                    jwt_secret=options_.jwt_secret,
                    https_enabled=options_.https_enabled,
                ),
            ),
            (
                r"/api/v1/users/([^/]*)",
                UserHandler,
                dict(
                    api=options_.api_host,
                    endpoint="users/{}",
                    http_client=httpclient.AsyncHTTPClient(),
                    jwt_secret=options_.jwt_secret,
                    https_enabled=options_.https_enabled,
                ),
            ),
            (
                r"/api/v1/tours/([^/]*)",
                ToursHandler,
                dict(
                    api=options_.api_host,
                    endpoint="tours/{}",
                    http_client=httpclient.AsyncHTTPClient(),
                    jwt_secret=options_.jwt_secret,
                    https_enabled=options_.https_enabled,
                    base_content_path=options_.base_content_path,
                ),
            ),
            (
                r"/api/v1/tours/([^/]*)/audio",
                AudioHandler,
                dict(
                    api=options_.api_host,
                    endpoint="tours/{}/audio",
                    http_client=httpclient.AsyncHTTPClient(),
                    jwt_secret=options_.jwt_secret,
                    https_enabled=options_.https_enabled,
                    base_content_path=options_.base_content_path,
                ),
            ),
            (
                r"/api/v1/tours/([^/]*)/images/([^/]*)",
                ImagesHandler,
                dict(
                    api=options_.api_host,
                    endpoint="tours/{}/images/{}",
                    http_client=httpclient.AsyncHTTPClient(),
                    jwt_secret=options_.jwt_secret,
                    https_enabled=options_.https_enabled,
                    base_content_path=options_.base_content_path,
                ),
            ),
            (r"/api/v1/tokens", WebSocketTokenHandler),
            (r"/updates", WebSocketHandler),
        ],
        cookie_secret=options_.cookie_secret,
        debug=options_.debug,
    )


def init_logging():
    """Initialize logging.

    Based on code found here:
    https://gist.github.com/kerma/a43526cc6f2ff1f07895b0b215d05931
    """

    # TODO: add logging formatter which includes timestamp
    access_log = logging.getLogger("tornado.access")
    access_log.propagate = False
    access_log.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler(sys.stdout)
    access_log.addHandler(stdout_handler)
