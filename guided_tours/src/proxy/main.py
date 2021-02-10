#!/usr/bin/env python3

import asyncio
import os
import logging

from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.options import define, options

from application import make_app, init_logging, init_borgs


define("api_host", type=str)
define("app_name", type=str)

define("base_content_path", type=str)
define("cookie_secret", type=str)
define("debug", type=bool)

define("https_enabled", type=bool)
define("jwt_secret", type=str)
define("port", type=int)
define("redis_host", type=str)


def main():
    logger = logging.getLogger("tornado.access")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    options.logging = None
    options.parse_config_file(f"{current_dir}/config/settings.conf")

    AsyncIOMainLoop().install()
    io_loop = asyncio.get_event_loop()

    init_logging()
    io_loop.run_until_complete(init_borgs(options, io_loop))

    app = make_app(options)
    app.listen(options.port)

    try:
        logger.info(f"Proxy service is running on port {options.port}")
        io_loop.run_forever()
    except KeyboardInterrupt:
        # cleanup
        pass


if __name__ == "__main__":
    main()
