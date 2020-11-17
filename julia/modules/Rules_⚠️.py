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


@register(pattern="^/rules$")
async def _(event):        
    if event.is_private:
      return
    global chatrules
    global chattitle
    chattitle = event.chat.title
    chat_id = event.chat_id
    chatrules = chat_id
    rules = sql.get_rules(chat_id)
    if rules:
        await event.reply("Contact me in PM to get this group's rules.", buttons=[[Button.url('Rules', url='t.me/MissJuliaRobot?start=rules')]])
    else:
        await event.reply(
            "The group admins haven't set any rules for this chat yet. "
            "This probably doesn't mean it's lawless though...!"
        )

@register(pattern="^/start rules$")
async def rules(event):       
       #print(chatrules)
       rules = sql.get_rules(chatrules)
       #print(rules)
       text = f"The rules for **{chattitle}** are:\n\n{rules}"       
       await event.respond(
            text, 
            parse_mode="markdown", 
            link_preview=False)

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


import os
from julia import tbot, CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
**Admin Only**
 - /setrules <rules>: set the rules for this chat
 - /clearrules: clears the rules for this chat
**Admin+Non-Admin**
 - /rules: get the rules for this chat
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
