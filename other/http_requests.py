import asyncio
import random
import urllib.parse
import uuid

from django.urls import reverse

from aiohttp import ClientSession


class User:
    def __init__(self, user_id, first_name, last_name):
        self.url = urllib.parse.urljoin("my_url", reverse("create_user"))
        payload = {}
        payload.update()
        payload["intent"] = "create"
        self.payload = payload


class VisitSession:
    def __init__(self, user_id, visit_session_id):
        self.url = urllib.parse.urljoin("my_url", reverse("create_visit_session", kwargs={"user_id": user_id}))
        payload = {}
        payload["intent"] = "create"
        self.payload = payload


class MyObject:
    def __init__(self, user_id, visit_session_id, creation_payload, object_type):
        kwr = {"user_id": user_id}
        self.payload = {}

OTHER_USER_DATA = []

async def create_user(i):
    async with ClientSession() as session:
        user_id = random.randint(7000, 15000)
        first_name = "Test"
        last_name = "tesst"
        user = User(user_id, first_name, last_name)
        async with session.post(user.url, json=user.payload) as response:
            response = await response.read()
            print(f"user #{i} is crated. Response {response}")
            visit_session_id = str(uuid.uuid4())
            visit_session = VisitSession(user_id, visit_session_id)
            async with session.post(visit_session.url, json=visit_session.payload) as response:
                response = await response.read()
                print(f"visit_session for user #{i} is crated. Response {response}")
                for payload, reverse_url in OTHER_USER_DATA:
                    obj = MyObject(user_id, visit_session_id, payload, reverse_url)
                    async with session.post(obj.url, json=obj.payload) as response:
                        response = await response.read()
                        print(f"{reverse_url} for user #{i} is crated. Response {response}")
        print(f"user #{i} is finished. First name is {first_name}, last name is {last_name}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(10):
        task = asyncio.ensure_future(create_user(i))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
