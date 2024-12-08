import asyncio
from json import loads
from os import chdir, sep
from typing import List

from httpx import AsyncClient


class User:
    url = ""
    platform = ""

    def __init__(self, name: str, pid: str, gid: str = "0") -> None:
        self.name = name
        self.pid = pid
        self.gid = gid

    async def _send_message(self, message: str) -> None:
        pass

    async def _send_image(self, file_url: str) -> None:
        pass

    async def _send_file(self, file_url: str) -> None:
        pass

    async def _send_voice(self, file_url: str) -> None:
        pass

    async def _ban_user(self) -> None:
        pass

    def send_message(self, message: str) -> None:
        asyncio.get_event_loop().create_task(self._send_message(message=message))

    def send_image(self, file_url: str) -> None:
        asyncio.get_event_loop().create_task(self._send_image(file_url=file_url))

    def send_file(self, file_url: str) -> None:
        asyncio.get_event_loop().create_task(self._send_file(file_url=file_url))

    def send_voice(self, file_url: str) -> None:
        asyncio.get_event_loop().create_task(self._send_voice(file_url=file_url))

    def ban_user(self) -> None:
        asyncio.get_event_loop().create_task(self._ban_user())

    def at(self) -> str:
        return ""


def get_url() -> dict:
    try:
        file = open("./config.json", "rb")
        config = loads(file.read())
        file.close()
    except FileNotFoundError:
        chdir(".." + sep + ".." + sep)
        file = open("./config.json", "rb")
        config = loads(file.read())
        file.close()
    return config


async def new_post(*args, **kwargs):
    async with AsyncClient() as client:
        result = await client.post(*args, **kwargs)
    return result
