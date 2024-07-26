from func.user.User import User
from func.user.event import bot
from func.user.event import func_dict
from . import *

help_info = """帮助
用别的功能的时候,用空格隔开各种参数
可以 /命令 help 查看帮助
"""


@bot(keyword="help", help_info=help_info)
async def bot_help(user: User, message: str) -> None:
    user.send_message("目前有以下功能:")
    func_lst = "\n".join(list(func_dict.keys()))
    user.send_message(func_lst)
    user.send_message("可以问 /help help 获取更多帮助")
