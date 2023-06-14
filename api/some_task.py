import asyncio
import aiohttp

import httpx

from typing import AsyncGenerator


async def some_task() -> AsyncGenerator[str, None]:
    yield "message 1"
    yield "message 2"

    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com") as response:
            text = await response.text()
            print(text)

    client = httpx.AsyncClient()

    breakpoint()
    response = await client.get("https://httpbin.org/get")
    print(response)

    # async with httpx.AsyncClient() as client:

    await asyncio.sleep(0.2)

    yield "message 3"
    yield "message 4"

    await asyncio.sleep(1)

    yield "message 5"
    yield "message 6"

    await asyncio.sleep(5)

    yield "message 7"
    yield "message 8"
