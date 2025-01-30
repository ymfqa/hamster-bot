from .User import User
from httpx import AsyncClient


class QUser(User):
    platform: str = "QQ"
    base_url: str = User.get_platform(platform)

    # 发送消息
    async def __send(self, message_type: str, message: str) -> None:
        async with AsyncClient() as c:
            # 发送群聊消息
            if self.gid:
                await c.post(
                    url=self.base_url + "/send_group_msg",
                    json={
                        "group_id": self.gid,
                        "message": [{"type": message_type, "data": {"text": message}}],
                    },
                )
            # 发送私聊消息
            else:
                await c.post(
                    url=self.base_url + "/send_private_msg",
                    json={
                        "user_id": self.pid,
                        "message": [{"type": message_type, "data": {"text": message}}],
                    },
                )

    # 发送文本消息
    async def send_message(self, message: str) -> None:
        await self.__send("text", message)

    # 发送图片消息
    async def send_image(self, url: str) -> None:
        await self.__send("image", url)

    # 发送语音消息
    async def send_voice(self, url: str) -> None:
        await self.__send("record", url)

    # 发送文件消息
    async def send_file(self, url: str) -> None:
        await self.__send("file", url)
