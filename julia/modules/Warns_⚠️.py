from julia import CMD_HELP
import asyncio
import html
import os
from telethon import *
from telethon.tl import *
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from julia.events import register
import julia.modules.sql.warns_sql as sql
from pymongo import MongoClient
from julia import MONGO_DB_URI


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


@register(pattern="^/warn")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass

        else:
            return
    warn_getter = event.text
    warn_reason = warn_getter.split(" ", maxsplit=1)[1]
    if not warn_reason:
        await event.reply("Please provide a reason for warning.")
        return
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(
        reply_message.sender_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: kick user")
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been kicked!".format(
                limit, reply_message.sender_id)
        else:
            logger.info("TODO: ban user")
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been banned!".format(
                limit, reply_message.sender_id)
    else:
        reply = "<u><a href='tg://user?id={}'>user</a></u> has {}/{} warnings... watch out!".format(
            reply_message.sender_id, num_warns, limit)
        if warn_reason:
            reply += "\nReason: {}".format(html.escape(warn_reason))
    #
    await event.reply(reply, parse_mode="html")


@register(pattern="^/getwarns$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass

        else:
            return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(
                num_warns, limit)
            text += "\r\n"
            text += reasons
            await event.reply(text)
        else:
            await event.reply("This user has {} / {} warning, but no reasons for any of them.".format(num_warns, limit))
    else:
        await event.reply("This user hasn't got any warnings!")


@register(pattern="^/removelastwarn$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if result and result[0] != 0:
        await event.reply("This user hasn't got any warnings!")
    sql.remove_warn(reply_message.sender_id, event.chat_id)

@register(pattern="^/resetwarns$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass

        else:
            return
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await event.reply("Warns for this user have been reset!")

global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /warn: warn a user
 - /removelastwarn: remove the last warn that a user has received
 - /getwarns: list the warns that a user has received
 - /resetwarns: reset all warns that a user has received
 - /warnmode <kick/ban>: set the warn mode for the chat
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
