from http import HTTPStatus
from os import environ
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from strawberry.fastapi import GraphQLRouter

from api.schema import schema
from redis import asyncio as aioredis  # type: ignore


app = FastAPI()

origins = [
    "https://studio.apollographql.com",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_context() -> dict[str, str]:
    redis = aioredis.from_url("redis://localhost")
    psub = redis.pubsub()
    pub = aioredis.Redis.from_url("redis://localhost", decode_responses=True)

    return {"redis_pub": pub, "redis_sub": psub}


graphql_app = GraphQLRouter[None, None](schema, path="/", context_getter=get_context)

app.include_router(graphql_app)


@app.middleware("http")
async def check_router_security(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    router_secret = environ.get("ROUTER_SECRET")
    if router_secret is None:
        return await call_next(request)
    if request.headers.get("Router-Authorization") != router_secret:
        return Response(status_code=HTTPStatus.UNAUTHORIZED)
    return await call_next(request)
