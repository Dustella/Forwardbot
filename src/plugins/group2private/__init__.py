from nonebot.adapters.cqhttp import Bot,GroupMessageEvent
from nonebot.plugin import on_message
from nonebot import get_driver
from .config import Config
import json
import re


global_config = get_driver().config
status_config = Config(**global_config.dict())

reply_session=on_message()

@reply_session.handle()
async def g2p(bot:Bot,event=GroupMessageEvent):
    raw=event.raw_message
    if 'CQ:reply' in raw:
        if str(event.message).startswith('#'): return 
        msgid=json.loads(event.json())["reply"]["message_id"]
        originnal_content=await bot.get_msg(message_id=msgid)
        txt=originnal_content['message'][0]['data']['text']
        sender_id_pattern = re.compile(r'(?<=\$).+(?=\n)')
        id_send=txt[sender_id_pattern.search(txt).start():sender_id_pattern.search(txt).end()]
        tosend=str(event.message).replace('[CQ:at,qq=2285047281] ', '')
        await bot.send_private_msg(user_id=id_send,message=tosend)



def get_sender(inp:str)->int:
    pass

