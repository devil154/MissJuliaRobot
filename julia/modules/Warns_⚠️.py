import asyncio
import html
from telethon import *
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from julia.events import register
import julia.modules.sql.warns_sql as sql


@register(pattern="^/warn ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    warn_reason = event.pattern_match.group(1)
    if not warn_reason:
      await event.reply("Please provide a reason for warning.")
      return
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(reply_message.sender_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: kick user")
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been kicked!".format(limit, reply_message.sender_id)
        else:
            logger.info("TODO: ban user")
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been banned!".format(limit, reply_message.sender_id)
    else:
        reply = "<u><a href='tg://user?id={}'>user</a></u> has {}/{} warnings... watch out!".format(reply_message.sender_id, num_warns, limit)
        if warn_reason:
            reply += "\nReason: {}".format(html.escape(warn_reason))
    #
    await event.reply(reply, parse_mode="html")


@register(pattern="^/getwarns$")
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(num_warns, limit)
            text += "\n\n"
            text += reasons
            await event.reply(text)
        else:
            await event.reply("This user has {} / {} warning, but no reasons for any of them.".format(num_warns, limit))
    else:
        await event.reply("This user hasn't got any warnings!")


@register(pattern="^/resetwarns$")
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await event.reply("Warns for this user have been reset!")
