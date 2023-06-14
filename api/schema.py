from __future__ import annotations

from typing import AsyncGenerator
import asyncio
import strawberry

from strawberry.types.info import Info


from .some_task import some_task


@strawberry.type
class Query:
    hello: list[str]


@strawberry.type
class StartTaskPayload:
    id: str


async def run_task(pub):
    channel = "status"

    async for message in some_task():
        print(f"(Writer) Publishing: {message}")
        await pub.publish(channel, message)
        await asyncio.sleep(1)
        print("(Writer) published")


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def start_task(self, info: Info) -> StartTaskPayload:
        pub = info.context["redis_pub"]

        asyncio.create_task(run_task(pub))

        return StartTaskPayload(id="1")


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def status(self, id: strawberry.ID, info: Info) -> AsyncGenerator[str, None]:
        pubsub = info.context["redis_sub"]

        await pubsub.subscribe("status")

        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)

            if message is not None:
                print(f"(Reader) Message Received: {message}")
                data = message["data"].decode()

                yield data

                if data == "finished🚀":
                    print("(Reader) STOP")
                    break


schema = strawberry.federation.Schema(
    Query, Mutation, Subscription, enable_federation_2=True
)
