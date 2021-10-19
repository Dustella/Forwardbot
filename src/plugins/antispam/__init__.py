# import nonebot
from nonebot import get_driver,on_keyword
from nonebot.exception import ActionFailed
from nonebot.adapters.cqhttp import Bot,MessageEvent
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

spam=on_keyword({"还没进群的同学","学校有重要事宜通知"})

@spam.handle()
async def anti_spam(bot:Bot,event:MessageEvent):
    this_message = event.message
    try:
        await bot.delete_msg(message_id=event.message_id)
        await spam.finish(f"可能的诈骗信息已识别，请勿上当。\n原消息已撤回,内容：\n{str(this_message)}")
    except ActionFailed as err:
        await spam.finish(f"可能的诈骗信息已识别，请勿上当。\n原消息无法撤回,内容：\n{str(this_message)}\n无法撤回原因：{str(err)}")
    pass