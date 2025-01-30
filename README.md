# HamsterBot

一个简单的，基于python+fastapi+httpx编写的异步小型机器人框架
目前支持
[QQ(napcat)](https://napneko.github.io/zh-CN/)，
且可自定义功能

## 使用方法

在config.json文件里面更改你的消息上报地址
然后
```
python3 start.py
```

## 插件编写方法

在func文件夹里仿照help.py的格式,使用`bot`装饰器和`user`类编写.py文件放在func文件夹
(当然,这个案例文件不存在,你可以造一个)
例如:
```
#./func/example.py 
from func.user.User import User
from func.user.event import bot
#帮助信息
help_info = """帮助信息
这只是一个案例,啥也不是
"""


@bot(keyword="example", help_info=help_info)
async def example(user: User, message: str) -> None:
    await user.send_message("这只是一个案例,啥也不是")
```
保存,运行,使用qq给你的bot发个`/example`
bot会回复你`user.send_message()`里面的话
