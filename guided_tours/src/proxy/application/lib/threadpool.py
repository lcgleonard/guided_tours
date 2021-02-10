import asyncio
import os
from concurrent.futures import ThreadPoolExecutor


async def run_in_threadpool(func, *args, **kwargs):
    # I'm running the method inside asyncio's thread pool
    # executor because it performs a blocking io action, e.g.
    # and action which writes the files to disk
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, *args, **kwargs)


async def remove_content_from_disk(server_file_location):
    await run_in_threadpool(os.remove, server_file_location)
