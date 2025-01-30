from json import load


# User类,以后可以通过继承它来扩展平台
class User:
    platform: str = ""
    base_url: str = ""

    # 获取base_url的方法
    @staticmethod
    def get_platform(platform: str) -> str:
        with open("./config.json", "r") as config:
            config = load(config)
            return config["url"][platform]

    # 初始化名称,个人号,群号(可选),
    def __init__(self, name: str, pid: int, gid: int | None = None) -> None:
        self.name = name
        self.pid = pid
        self.gid = gid

    # 发送文本消息
    async def send_message(self, message: str) -> None:
        pass

    # 发送图片消息
    async def send_image(self, url: str) -> None:
        pass

    # 发送语音消息
    async def send_voice(self, url: str) -> None:
        pass

    # 发送文件消息
    async def send_file(self, url: str) -> None:
        pass
