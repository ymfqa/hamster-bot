from typing import List
from func.user.User import *
from os.path import split
from json import dumps


class QUser(User):
    platform = "QQ"
    url = get_url()["send_url"][platform]

    async def _send_message(self, message: str) -> None:
        if self.gid != "0":
            await new_post(
                url=self.url + "/send_group_msg",
                data={"group_id": self.gid, "message": message},
            )
        else:
            await new_post(
                url=self.url + "/send_private_msg",
                data={"user_id": self.pid, "message": message},
            )

    async def _send_image(self, file_url: str) -> None:
        await self._send_message(f"[CQ:image,file={file_url},url={file_url}]")

    async def _send_voice(self, file_url: str) -> None:
        await self._send_message(f"[CQ:record,file={file_url},url={file_url}]")

    async def _send_file(self, file_url: str) -> None:
        if self.gid != "0":
            await new_post(
                url=self.url + "/upload_group_file",
                data={
                    "group_id": self.gid,
                    "file": file_url,
                    "name": split(file_url)[-1],
                },
            )
        else:
            await new_post(
                url=self.url + "/upload_private_file",
                data={
                    "user_id": self.pid,
                    "file": file_url,
                    "name": split(file_url)[-1],
                },
            )

    async def _ban_user(self) -> None:
        if self.gid == "0":
            return None
        await new_post(
            url=self.url + "/set_group_ban",
            data={"group_id": self.gid, "user_id": self.pid, "duration": 60},
        )

    def at(self) -> str:
        return f"[CQ:at,qq={self.pid}]"
