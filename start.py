import asyncio
from user.QUser import QUser
from user.User import User
from func.event import func_dict, func_help, log_lst
from importlib import import_module
from os import listdir
from asyncio import sleep
from time import strftime, localtime, time
from fastapi import FastAPI, Request
from json import loads
import uvicorn

# 存储用户
qq_users = {}  # QQ用户

# 批量导入函数模块,不然无法使用函数
file_lst = listdir("./func/")
# 忽略event,不需要导入这个
file_lst.remove("event.py")
# 忽略python生成的文件夹
if "__pycache__" in file_lst:
    file_lst.remove("__pycache__")
# 去除后缀名(.py)
file_lst = map(lambda x: x[0:-3], file_lst)
# 批量导入
for i in file_lst:
    import_module("func." + i)


async def judge(user: User, message: str) -> None:
    # 提取关键词
    keyword = message.split()[0]
    # 判断关键词是否存在
    if func_dict.get(keyword, None):
        # 提取剩余信息 没有的话返回空字符串
        new_message = (
            len(message.split(maxsplit=1)) > 1 if message.split(maxsplit=1) else ""
        )
        # 如果剩余信息是help,直接发送帮助信息
        if new_message == "help":
            await user.send_message(func_help[keyword])
        # 执行功能函数
        else:
            await func_dict[keyword](user, message)


# 日志保存函数
async def log_save() -> None:
    while True:
        # 30秒写入一次
        await sleep(30)
        # 写入到 年-月-日.log
        with open(
            "./log/" + strftime(r"%Y-%m-%d", localtime(time())) + ".log",
            "a+",
        ) as log:
            # 写入文件
            log.writelines(log_lst)
            # 写入以后清理缓存
            log_lst.clear()


app = FastAPI(
    title="hamster-bot",
    summary="""只是一个机器人框架而已""",
    redoc_url=None,
)


@app.post(
    "/qqbot",
    tags=["qqbot"],
    summary="qq机器人接口",
)
async def qqbot(
    request: Request,
):
    # 获取原始json数据
    user_info = await request.json()
    # 获取个人id,群聊id,用户名和原始消息
    pid = user_info["user_id"]
    gid = user_info.get("group_id", None)
    username = user_info["sender"]["nickname"]
    message = user_info["raw_message"]
    # 判断用户是否存在
    if qq_users.get(str(gid) + str(pid), None):
        user = qq_users.get(str(gid) + str(pid), None)
    else:
        user = QUser(username, pid, gid)
    # 判断是否执行功能函数(是的话顺便执行了)
    await judge(user, message)
    return {}


if __name__ == "__main__":
    # 获取事件循环
    loop = asyncio.get_event_loop()
    # 运行保存日志
    loop.create_task(log_save())
    # 读取配置文件
    with open("./config.json", "r") as config:
        config = loads(config.read())
        host = config["host"]
        port = config["port"]
    # 获取ASGI服务器配置
    config = uvicorn.Config("start:app", host=host, port=port)
    # 获取ASGI服务实例
    server = uvicorn.Server(config)
    loop.create_task(server.serve())
    print("running!")
    loop.run_forever()
