from func.user.User import *


class WeUser(User):
    platform = "WeChat"
    url = get_url()["send_url"][platform]
    headers = {"content-type": "application/json"}

    async def __send_message(self, message: str) -> None:
        if self.gid != "0":
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.gid,
                    "isRoom": True,
                    "data": {"content": message},
                },
            )
        else:
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.pid,
                    "isRoom": False,
                    "data": {"content": message},
                },
            )

    async def __send_file(self, file_url: str) -> None:
        if self.gid != "0":
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.gid,
                    "isRoom": "true",
                    "data": {"type": "fileUrl", "content": file_url},
                },
            )
        else:
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.pid,
                    "isRoom": "false",
                    "data": {"type": "fileUrl", "content": file_url},
                },
            )

    async def __send_image(self, file_url: str) -> None:
        if self.gid != "0":
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.gid,
                    "isRoom": "true",
                    "data": {"type": "fileUrl", "content": file_url},
                },
            )
        else:
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.pid,
                    "isRoom": "false",
                    "data": {"type": "fileUrl", "content": file_url},
                },
            )

    async def __send_voice(self, file_url: str) -> None:
        if self.gid != "0":
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.gid,
                    "isRoom": "true",
                    "data": {"type": "fileUrl", "content": file_url},
                },
            )
        else:
            await new_post(
                url=self.url,
                headers=self.headers,
                json={
                    "to": self.pid,
                    "isRoom": "false",
                    "data": {"type": "fileUrl", "content": file_url},
                },
            )

    async def __ban_user(self) -> None:  # 微信bot暂时不支持禁言
        pass

    def send_message(self, message: str) -> None:
        asyncio.get_event_loop().create_task(self.__send_message(message=message))

    def send_image(self, file_url: str) -> None:
        asyncio.get_event_loop().create_task(self.__send_image(file_url=file_url))

    def send_file(self, file_url: str) -> None:
        asyncio.get_event_loop().create_task(self.__send_file(file_url=file_url))

    def send_voice(self, file_url: str) -> None:
        asyncio.get_event_loop().create_task(self.__send_voice(file_url=file_url))

    def ban_user(self) -> None:
        asyncio.get_event_loop().create_task(self.__ban_user())

    def at(self) -> str:
        return "@" + self.pid
