from nonebot.adapters.cqhttp import Bot,PrivateMessageEvent
from nonebot.plugin import on
from .config import Config
from nonebot import on_message,get_driver

callin_session=on_message()

global_config = get_driver().config
status_config = Config(**global_config.dict())

@callin_session.handle()
async def p2g(bot:Bot,event:PrivateMessageEvent):
    sender_id=event.get_user_id()
    sender_nick=event.sender.nickname
    message_content=event.get_message()
    fwd_str=f'{sender_nick}: \n${sender_id}\n{message_content}'
    if int(event.sender.user_id) == int(bot.self_id):
        fwd_str=f'我发送了:\n{message_content}'
    print(fwd_str)
    await bot.send_group_msg(group_id=status_config.group_id,message=fwd_str)