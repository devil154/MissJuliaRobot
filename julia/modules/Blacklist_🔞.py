from julia import tbot
import re
from telethon import events
import julia.modules.sql.blacklist_sql as sql
from julia.events import register
from telethon import types
from telethon.tl import functions
from julia import tbot


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


@tbot.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    # TODO: exempt admins from locks
    if await is_register_admin(event.input_chat, event.message.sender_id):
        return

    name = event.text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        print(re.search(pattern, name, flags=re.IGNORECASE))
        if re.search(pattern, name, flags=re.IGNORECASE):    
            try:
                await event.delete()
            except Exception as e:
                print(e)


@register(pattern="^/addblacklist ((.|\n)*)")
async def on_add_black_list(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    text = event.pattern_match.group(1)
    to_blacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await event.reply(
        "Added {} triggers to the blacklist in the current chat".format(
            len(to_blacklist)
        )
    )


@register(pattern="^/listblacklist$")
async def on_view_blacklist(event):
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "**Blacklists in the Current Chat:\n**"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "No BlackLists. Start Adding using /addblacklist"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="BlackLists in the Current Chat",
                reply_to=event,
            )
            await event.delete()
    else:
        await event.reply(OUT_STR)


@register(pattern="^/rmblacklist ((.|\n)*)")
async def on_delete_blacklist(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(event.chat_id, trigger.lower()):
            successful += 1
    await event.reply(f"Removed {successful} / {len(to_unblacklist)} from the blacklist")
    
   
import os
from julia import CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
**Admin Only**
 - /addblacklist <trigger> : blacklists the trigger
 - /rmblacklist <trigger> : stop blacklisting a certain blacklist trigger
 - /listblacklist: list all active blacklist filters

**Example:**
 - /addblacklist the admins suck: This will remove "the admins suck" everytime some non-admin types it
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
