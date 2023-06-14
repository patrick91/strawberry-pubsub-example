import asyncio

import httpx

from typing import AsyncGenerator


async def some_task() -> AsyncGenerator[str, None]:
    yield "message 1"
    yield "message 2"

    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(response)

    await asyncio.sleep(0.2)

    yield "message 3"
    yield "message 4"

    await asyncio.sleep(1)

    yield "message 5"
    yield "message 6"

    await asyncio.sleep(5)

    yield "message 7"
    yield "message 8"
