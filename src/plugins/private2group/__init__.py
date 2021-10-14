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
    # last_message_user=(await bot.get_group_msg_history(group_id=status_config.group_id))["messages"][19]["user_id"]
    # last_message=(await bot.get_group_msg_history(group_id=status_config.group_id))["messages"][19]["raw_message"]
    # lite_flag=(str(last_message_user)==str(bot.self_id)) and (str(last_message).find("Sent_to")==-1) and (last_callin_session==event.get_user_id())

    user_info=f"From: {event.sender.nickname}\n@{event.get_user_id()}#{event.message_id}\n"
    message_type=json.loads(event.json())["message"][0]["type"]
    if message_type=="video":
        await bot.send_group_msg(group_id=status_config.group_id,message=f"{user_info}\n[视频消息]")
    elif message_type=="forward":
        await bot.send_group_msg(group_id=status_config.group_id,message=f"{user_info}\n[转发消息]")
    elif message_type=="xml":
        await bot.send_group_msg(group_id=status_config.group_id,message=f"{user_info}\n[xml消息]")
    fwd_str=(f'{user_info}\n{event.get_message()}',f"{event.get_message()}")[0]

    last_callin_session=event.get_user_id()
    await bot.send_group_msg(group_id=status_config.group_id,message=fwd_str)
    await callin_session.finish()

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
