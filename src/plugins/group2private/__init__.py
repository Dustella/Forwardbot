from nonebot import get_driver,on_message
from nonebot.adapters.cqhttp import Bot,GroupMessageEvent,Message
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.exception import ActionFailed
import re
from .config import Config


global_config = get_driver().config
config = Config(**global_config.dict())
callin_session =on_message(rule=to_me(),priority=1)

@callin_session.handle()
async def handle_first_message(bot:Bot,event:GroupMessageEvent,state:T_State):
    if str(event.message).startswith('#'):await callin_session.finish()
    # if reply is a comment, do nothing
    origin=str(event.reply.message)
    sender_id_pattern = re.compile(r'(?<=\@).+(?=\n)')
    message_id_pattern = re.compile(r'(?<=#).+(?=\n)')
    state["target_id"]=origin[sender_id_pattern.search(origin).start():sender_id_pattern.search(origin).end()]
    state["message_id"]=origin[message_id_pattern.search(origin).start():message_id_pattern.search(origin).end()]
    # get reply target_id, stored in state
    print(state)
    if str(event.message)=="pic":
        state["is_pic"]=True
    elif str(event.message)=="del" or str(event.message)=="recall":
        try:
            await bot.delete_msg(message_id=state["message_id"])
            await callin_session.finish()
        except ActionFailed as err:
            await callin_session.finish(f"Error encountered, {err}")
    else:
        state["message"] =event.message
        state["is_pic"]=False
        # handle pictures


@callin_session.got("message",prompt="Send a picture")
async def send_picture(bot:Bot,event:GroupMessageEvent,state:T_State):
    if state["is_pic"] \
    and not "[CQ:image" in str(state["message"] \
    and not "cancel" in str(state["message"])):
        callin_session.reject("Please send a picture")
        # if message is not a picture, reject it

    try:
        await bot.send_private_msg(user_id=state["target_id"],message=state["message"])
        await callin_session.finish()
        # final send
    except ActionFailed as err:
        await bot.finish(f"Error encountered, {err}")
