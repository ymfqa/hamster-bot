from typing import Callable, Dict, Union
from func.user.QUser import QUser
from func.user.WeUser import WeUser
from func.user.User import User, get_url
from func.user.event import log_lst, func_dict, func_help
from time import strftime, localtime, time
from json import dumps, loads
from os import listdir
from importlib import import_module
import asyncio

try:
    from quart import Quart, request
except ModuleNotFoundError:
    __import__("os").system("pip install quart")
    from quart import Quart, request

# 查看监听url
listen_url = get_url()["listen_url"]

# 存储用户
we_user_dict: Dict[str, WeUser] = {}  # 微信用户
qq_user_dict: Dict[str, QUser] = {}  # QQ用户

# 批量导入函数模块,不然无法使用函数
file_lst = listdir("./func/")
file_lst.remove("user")
if "__pycache__" in file_lst:
    file_lst.remove("__pycache__")
file_lst = map(lambda x: x[0:-3], file_lst)
for i in file_lst:
    import_module("func." + i)


# 判断关键字函数
async def judge(user: User, message: str) -> Union[Callable, None]:
    if message.split(" ")[0] in func_dict.keys():
        if len(message.split(" ")) > 1:
            if message.split(" ")[1] == "help":
                user.send_message(func_help[message.split(" ")[0]])
                return None
            else:
                return func_dict[message.split(" ")[0]]
        else:
            return func_dict[message.split(" ")[0]]
    else:
        return None


# 日志保存函数
async def log_save() -> None:
    while True:
        await asyncio.sleep(30)
        with open(
            "./log/" + strftime(r"%Y-%m-%d", localtime(time())) + ".log",
            "a+",
        ) as log_file:
            log_file.writelines(log_lst)
            log_lst.clear()


# 获取事件循环
loop = asyncio.get_event_loop()

# 建立服务
app = Quart(__name__)


@app.route("/webot", methods=["GET", "POST"])
async def we_message_get():  # 微信消息处理
    if (await request.form)["type"] != "text":  # 判断消息是否为文字,不是则直接跳过
        return dumps("{}")
    message = (await request.form)["content"]
    if dict(loads(dict(await request.form)["source"]))["room"]:
        gid = dict(loads(dict(await request.form)["source"]))["room"]["payload"][
            "topic"
        ]
    else:
        gid = "0"
    name = str(
        dict(loads(dict(await request.form)["source"]))["from"]["payload"]["name"]
    )
    pid = name
    if gid + pid in we_user_dict.keys():
        user = we_user_dict[gid + pid]
    else:  # 没有用户则新建用户
        user = WeUser(name=name, pid=pid, gid=gid)
        we_user_dict[gid + pid] = user
    func = await judge(user=user, message=message)
    if not func:  # 如果没有功能则提前跳过
        return dumps("{}")
    loop.create_task(func(user, message))

    return dumps("{}")


@app.route("/qqbot", methods=["GET", "POST"])
async def qq_message_get():  # QQ消息处理
    message = (await request.get_json())["raw_message"]
    if (await request.get_json())["message_type"] == "group":
        gid = str((await request.get_json())["group_id"])
    else:
        gid = "0"
    name = (await request.get_json())["sender"]["nickname"]
    pid = str((await request.get_json())["user_id"])
    if gid + pid in qq_user_dict.keys():
        user = qq_user_dict[gid + pid]
    else:  # 没有用户则新建用户
        user = QUser(name=name, pid=pid, gid=gid)
        qq_user_dict[gid + pid] = user
    func = await judge(user=user, message=message)
    if not func:  # 如果没有功能则提前跳过
        return dumps("{}")
    loop.create_task(func(user, message))

    return dumps("{}")


async def listen_server():
    try:
        loop.create_task(log_save())
        await app.run_task(host=listen_url.split(":")[0], port=listen_url.split(":")[1])
    except Exception as error:
        loop.stop()
        loop.close()
        __import__("sys").exit()


if __name__ == "__main__":
    loop.run_until_complete(loop.create_task(listen_server()))
