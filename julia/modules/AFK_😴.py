from julia.modules.sql import afk_sql as sql

from telegram.error import BadRequest

import time
from telethon import types
from telethon.tl import functions
from julia import tbot
from julia.events import register

from pymongo import MongoClient
from julia import MONGO_DB_URI
from telethon import events

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client['test']
approved_users = db.approve

async def is_register_admin(chat, user):
    try:
        if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

            return isinstance(
                (
                    await tbot(functions.channels.GetParticipantRequest(chat, user))
                ).participant,
                (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
            )
        if isinstance(chat, types.InputPeerChat):

            ui = await tbot.get_peer_id(user)
            ps = (
                await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
            ).full_chat.participants.participants
            return isinstance(
                next((p for p in ps if p.user_id == ui), None),
                (types.ChatParticipantAdmin, types.ChatParticipantCreator),
            )
        return False
    except Exception:
        return False


@register(pattern="^/afk ?(.*)")
async def _(event):
    send = await event.get_sender()
    sender = await tbot.get_entity(send)
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch['id']
        userss = ch['user']
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    else:
      return

    cmd = event.pattern_match.group(1)
    if cmd:
        reason = cmd
    else:
        reason = ""
    
    fname = sender.first_name
    notice = ""
    if len(reason) > 100:
        reason = reason[:100]
        notice = "{fname} your afk reason was shortened to 100 characters."
    else:
        reason = ""
    start_time = time.time()
    sql.set_afk(sender.id, reason, start_time)

    try:
        await event.reply(
            "**{} is now AFK !**\n\n{}".format(fname, notice),
            parse_mode="markdown",
        )
    except BadRequest:
        pass


@tbot.on(events.NewMessage(pattern="/noafk$"))
async def _(event):
    send = await event.get_sender()
    sender = await tbot.get_entity(send)

    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch['id']
        userss = ch['user']
        
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    else:
      return

    res = sql.rm_afk(sender.id)
    if res:

        firstname = sender.first_name
        try:
            text = "**{} is no longer AFK !**".format(firstname)
            await event.reply(text, parse_mode="markdown")
        except BaseException:
            return

from telethon.tl.types import MessageEntityMention

@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    send = await event.get_sender()
    sender = event.sender_id
    msg = str(event.text)
    global userid
    global let

    if event.reply_to_msg_id:
       reply = await event.get_reply_message()
       userid = reply.sender_id 
    else:
     try:
      for (ent, txt) in event.get_entities_text():
        if ent.offset != 0:
            break
        if isinstance(ent, types.MessageEntityMention):                       
          c = txt
          a = c.split()[0]
        let = await tbot.get_entity(a)
        userid = let.id       
     except Exception:
       return
    
    if sender == userid:
       return

    if event.is_group:
       pass
    else:
       return  

    if sql.is_afk(userid):
        user = sql.check_afk_status(userid)
        if not user.reason:
            etime = user.start_time
            elapsed_time = time.time() - float(etime)
            final = time.strftime("%Hh: %Mm: %Ss", time.gmtime(elapsed_time))
            try:
              fst_name = let.first_name
            except:
              fst_name = "This user"
            res = "**{} is AFK !**\n\n**Last seen**: {}".format(fst_name, final)
     
            await event.reply(res, parse_mode="markdown")
        else:
            etime = user.start_time
            elapsed_time = time.time() - float(etime)
            final = time.strftime("%Hh: %Mm: %Ss", time.gmtime(elapsed_time))
            try:
              fst_name = let.first_name
            except:
              fst_name = "This user"
            res = "**{} is AFK !**\n\n**Reason**: {}\n\n**Last seen**: {}".format(
                fst_name, user.reason, final
            )
            await event.reply(res, parse_mode="markdown")
    userid = None # after execution

import inspect
import logging
import re, os
from pathlib import Path
from julia import tbot, CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
 - /afk <reason>: mark yourself as AFK(Away From Keyboard)
 - /noafk: unmark yourself as AFK(Away From Keyboard)
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
