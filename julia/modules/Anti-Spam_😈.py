import html
from julia.modules.sql import cleaner_sql as sql
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
from telethon import types, events
from telethon.tl import *
from julia import *

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["test"]
approved_users = db.approve

async def can_change_info(message):
        result = await tbot(
            functions.channels.GetParticipantRequest(
                channel=message.chat_id,
                user_id=message.sender_id,
            )
        )
        p = result.participant
        return isinstance(p, types.ChannelParticipantCreator) or (
            isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
        )

async def is_register_admin(chat, user):
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
    return None


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch['id']
        userss = ch['user']
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            return
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            pass
    else:
      return

    if str(event.sender_id) == "1246850012":
        return

    if event.sender_id == OWNER_ID:
        return

    for (ent, txt) in event.get_entities_text():
        if ent.offset != 0:
            break
        print (txt)
        if isinstance(ent, types.MessageEntityBotCommand):   
          print("right")                    
          pass
        else:
          return
  
    if sql.is_enabled(event.chat_id):
       await event.delete()


@register(pattern="^/cleanbluetext ?(.*)")
async def _(event):
    if event.is_group:
            if not await can_change_info(message=event):
                return
    else:
       return
    args = event.pattern_match.group(1)
    if args:
        val = args
        if val in ("off", "no"):
            sql.set_cleanbt(event.chat_id, False)
            reply = "Bluetext cleaning has been disabled for <b>{}</b>".format(
                html.escape(event.chat.title)
            )
            await event.reply(reply, parse_mode="html")

        elif val in ("yes", "on"):
            sql.set_cleanbt(event.chat_id, True)
            reply = "Bluetext cleaning has been enabled for <b>{}</b>".format(
                html.escape(event.chat.title)
            )
            await event.reply(reply, parse_mode="html")

        else:
            reply = "Invalid argument.Accepted values are 'yes', 'on', 'no', 'off'"
            await event.reply(reply, parse_mode="html")
    else:
        clean_status = sql.is_enabled(event.chat_id)
        clean_status = "Enabled" if clean_status else "Disabled"
        reply = "Bluetext cleaning for <b>{}</b> : <b>{}</b>".format(
            event.chat.title, clean_status
        )
        await event.reply(reply, parse_mode="html")


__help__ = """
 - /cleanbluetext <on/off/yes/no>: clean commands from non-admins after sending
 - /ignorecleanbluetext <word>: prevent auto cleaning of the command
 - /unignorecleanbluetext <word>: remove prevent auto cleaning of the command
 - /listcleanbluetext: list currently whitelisted commands
"""
