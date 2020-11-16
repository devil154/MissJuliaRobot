from typing import Optional
import julia.modules.sql.rules_sql as sql
from telethon import *
from telethon.tl import *
from julia import *

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


@register(pattern="^/rules")
async def _(event):        
    chat_id = event.chat_id
    await send_rules(event, chat_id)


async def send_rules(event, chat_id, from_pm=False):
    user = event.sender_id	
    rules = sql.get_rules(chat_id)
    text = f"The rules for **{event.chat.title}** are:\n\n{rules}"

    if from_pm and rules:
        await tbot.send_message(
            user, text, parse_mode="markdown", link_preview=True
        )
    elif from_pm:
        await tbot.send_message(
            user,
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!",
        )
    elif rules:
        await event.reply(
            "Contact me in PM to get this group's rules.", buttons=[
              [Button.inline('Rules', data='give_rules')]])
    else:
        await event.reply(
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!"
        )

@tbot.on(events.CallbackQuery(pattern=r'give_rules'))
async def give_rules(event):
    if not event.is_private:
       rules = sql.get_rules(event.chat_id)
       text = f"The rules for **{event.chat.title}** are:\n\n{rules}"       
       await tbot.send_message(
            event.sender_id,
            text, 
            parse_mode="markdown", 
            link_preview=True,
        )
    else:
        return

@register(pattern="^/setrules")
async def _(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    chat_id = event.chat_id
    raw_text = event.text
    args = raw_text.split(None, 1)  
    if len(args) == 2:
        txt = args[1]
        sql.set_rules(chat_id, txt)
        await event.reply("Successfully set rules for this group.")


@register(pattern="^/clearrules$")
async def _(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    chat_id = event.chat_id
    sql.set_rules(chat_id, "")
    await event.reply("Successfully cleared rules for this chat !")
