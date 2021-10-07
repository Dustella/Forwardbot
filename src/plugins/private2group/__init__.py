from nonebot.adapters.cqhttp import Bot,Event,PrivateMessageEvent,Message
from nonebot.plugin import on,on_message
from .config import Config
from nonebot import get_driver
import json

last_callin_session=0
callin_session=on_message()
message_sent=on(type="message_sent")

global_config = get_driver().config
status_config = Config(**global_config.dict())

@callin_session.handle()
async def p2g(bot:Bot,event:PrivateMessageEvent):
    global last_callin_session
    sender_id=event.get_user_id()
    sender_nick=event.sender.nickname
    message_content=event.get_message()
    fwd_str=f'From: {sender_nick}\n@{sender_id}\n\n{message_content}'
    last_callin_session=event.sender.user_id
    await bot.send_group_msg(group_id=status_config.group_id,message=fwd_str)

@message_sent.handle()
async def message_sent_fwd(bot:Bot,event:Event):
    this_event=json.loads(event.json())
    if this_event['sub_type']!="friend": return
    msgcontent=this_event['message']
    msgid=this_event['message_id']
    target_id=this_event['target_id']
    target_nick=(await bot.get_stranger_info(user_id=target_id))['nickname']
    print(target_nick,target_id)
    tosend=Message(msgcontent)
    fwd_str=f'Sent_to: {target_nick}\n@{target_id}#{msgid}\n\n{tosend}'
    print(fwd_str)
    await bot.send_group_msg(group_id=status_config.group_id,message=fwd_str)
