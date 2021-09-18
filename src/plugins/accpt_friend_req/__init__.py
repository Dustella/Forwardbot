# import nonebot
from nonebot import get_driver, on_request
from nonebot.adapters.cqhttp import FriendRequestEvent,Bot
from nonebot.plugin import on_request
from nonebot.rule import to_me
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

new_friend=on_request()

@new_friend.handle()
async def accptfd(event:FriendRequestEvent,bot:Bot):
    print('lala')
    api_flag=event.flag
    await bot.set_friend_add_request(flag=api_flag,approve=True)
    print(api_flag)
    # await bot.set_friend_add_request()
    # pass
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
