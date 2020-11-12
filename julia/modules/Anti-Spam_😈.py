import html
from julia.modules.sql import cleaner_sql as sql
from pymongo import MongoClient
from julia import MONGO_DB_URI
from julia.events import register
from telethon import *
from telethon.tl import *
from julia import *
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["test"]
approved_users = db.approve

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


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    chats = approved_users.find({})
    for c in chats:
        iiid = c["id"]
        usersss = c["user"]
        if str(event.sender_id) in str(usersss) and str(event.chat_id) in str(iiid):
            return
    if event.sender_id == 1246850012:
        return
    if event.sender_id == OWNER_ID:
        return
    try:
      for (ent, txt) in event.get_entities_text():
        if ent.offset != 0:
            break
        if isinstance(ent, types.MessageEntityBotCommand):                       
            pass
        else:
            return
    except Exception: # just in case of flood wait
          return
  
    if sql.is_enabled(event.chat_id):
          await event.delete()


@register(pattern="^/cleanbluetext ?(.*)")
async def _(event):
    args = event.pattern_match.group(1)
    if args:
        val = args[0].lower()
        if val in ("off", "no"):
            sql.set_cleanbt(event.chat_id, False)
            reply = "Bluetext cleaning has been disabled for <b>{}</b>".format(
                html.escape(event.chat.title)
            )
            await event.reply(reply)

        elif val in ("yes", "on"):
            sql.set_cleanbt(event.chat_id, True)
            reply = "Bluetext cleaning has been enabled for <b>{}</b>".format(
                html.escape(event.chat.title)
            )
            await event.reply(reply)

        else:
            reply = "Invalid argument.Accepted values are 'yes', 'on', 'no', 'off'"
            await event.reply(reply)
    else:
        clean_status = sql.is_enabled(event.chat_id)
        clean_status = "Enabled" if clean_status else "Disabled"
        reply = "Bluetext cleaning for <b>{}</b> : <b>{}</b>".format(
            event.chat.title, clean_status
        )
        await event.reply(reply)


__help__ = """
 - /cleanbluetext <on/off/yes/no>: clean commands from non-admins after sending
 - /ignorecleanbluetext <word>: prevent auto cleaning of the command
 - /unignorecleanbluetext <word>: remove prevent auto cleaning of the command
 - /listcleanbluetext: list currently whitelisted commands
"""

