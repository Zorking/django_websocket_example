import asyncio
import json
import logging
import os
from asyncio import sleep
from urllib.parse import urljoin

import aiohttp
import redis
import requests
from aiohttp import web, WSCloseCode

URL = "http://web:8000"
REDIS_SERVER = redis.Redis.from_url(os.getenv("REDIS_HOST_BASE_URL", ""))

routes = web.RouteTableDef()


async def websocket_auth(request, path):
    token = request.match_info["token"]
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    response = requests.get(urljoin(URL, path),
                            headers={"Authorization": f"Bearer {token}"})
    if not response.ok:
        await ws.close(message=b"Can't connect")
        return ws, None
    return ws, response


async def read_subscription(ws, subscription):
    while True:
        message = subscription.get_message()
        if message and isinstance(message["data"], bytes):
            subscription_message = json.loads(message["data"])
            await ws.send_json(subscription_message)
            await ws.close()
        await sleep(1)


@routes.get("/{token}/ws")
async def websocket_connection(request):
    ws, response = await websocket_auth(request, "auth/")
    if not response:
        return ws
    subscription = REDIS_SERVER.pubsub()
    subscription.subscribe("user_id")
    task = asyncio.create_task(read_subscription(ws, subscription))
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT and msg.data == "close":
            break
    task.cancel()
    await ws.close()
    subscription.unsubscribe("user_id")
    await ws.close()
    return ws


async def on_shutdown(app_instance):
    for key, value in app_instance["websockets"].items():
        logging.info(f"Connection with {key} is closed due to server shutdown.")
        await value.get("ws").close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")


app = web.Application()
app.add_routes(routes)
app.on_shutdown.append(on_shutdown)
web.run_app(app)
