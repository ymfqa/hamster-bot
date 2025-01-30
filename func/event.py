from typing import Callable
from traceback import format_exc
from time import strftime, localtime, time

log_lst = []  # 缓存日志
func_dict = {}  # 存储函数
func_help = {}  # 存储函数帮助信息


# 日志生成
def log_format(log_type: str, log_info: str) -> str:
    now = strftime(r"%Y-%m-%d %H:%M:%S", localtime(time()))
    return "[" + log_type + "](" + now + "):" + log_info


# bot函数装饰器
def bot(keyword: str, help_info: str) -> Callable:
    def wrapper1(func: Callable) -> Callable:
        async def wrapper2(*args, **kwargs):
            try:
                # 执行功能函数
                await func(*args, **kwargs)
            except Exception:
                # 发生错误记录错误日志
                log = log_format("ERROR", format_exc())
            else:
                # 正常运行记录正常日志
                log = log_format("Using", keyword)
            print(log)
            log_lst.append(log + "\n")

        func_dict["/" + keyword] = wrapper2
        func_help["/" + keyword] = help_info
        return wrapper2

    return wrapper1
