from func.user.User import *


class WeUser(User):
    platform = "WeChat"
    url = get_url()["send_url"][platform]
    headers = {"content-type": "application/json"}

    async def _send_message(self, message: str) -> None:
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

    async def _send_file(self, file_url: str) -> None:
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

    async def _send_image(self, file_url: str) -> None:
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

    async def _send_voice(self, file_url: str) -> None:
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

    # 微信bot暂时不支持禁言

    def at(self) -> str:
        return "@" + self.pid
