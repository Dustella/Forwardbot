from nonebot.adapters.cqhttp import Bot,Event,PrivateMessageEvent,Message
from nonebot.plugin import on,on_message
from .config import Config
from nonebot import get_driver
import json

callin_session=on_message()
message_sent=on(type="message_sent")

global_config = get_driver().config
status_config = Config(**global_config.dict())

@callin_session.handle()
async def p2g(bot:Bot,event:PrivateMessageEvent):
    sender_id=event.get_user_id()
    sender_nick=event.sender.nickname
    message_content=event.get_message()
    fwd_str=f'{sender_nick}: \n${sender_id}\n{message_content}'
    await bot.send_group_msg(group_id=status_config.group_id,message=fwd_str)

@message_sent.handle()
async def message_sent_fwd(bot:Bot,event:Event):
    this_event=json.loads(event.json())
    msgcontent=this_event['message']
    tosend=Message(msgcontent)
    fwd_str=f'我发送了:\n{tosend}'
    await bot.send_group_msg(group_id=status_config.group_id,message=fwd_str)
