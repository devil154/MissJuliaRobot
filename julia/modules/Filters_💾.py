from julia import tbot
import asyncio
import re

from telethon import utils
from telethon.tl import types
from telethon import events
from julia.modules.sql.filters_sql import (
    add_filter,
    get_all_filters,
    remove_filter,
)

DELETE_TIMEOUT = 0

TYPE_TEXT = 0

TYPE_PHOTO = 1

TYPE_DOCUMENT = 2


global last_triggered_filters

last_triggered_filters = {}  # pylint:disable=E0602
from telethon.tl import functions
from julia import tbot
from julia.events import register

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
async def on_snip(event):

    global last_triggered_filters

    name = event.raw_text

    if event.chat_id in last_triggered_filters:

        if name in last_triggered_filters[event.chat_id]:

            return False

    snips = get_all_filters(event.chat_id)

    if snips:

        for snip in snips:

            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"

            if re.search(pattern, name, flags=re.IGNORECASE):

                if snip.snip_type == TYPE_PHOTO:

                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )

                elif snip.snip_type == TYPE_DOCUMENT:

                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )

                else:

                    media = None

                event.message.id

                if event.reply_to_msg_id:

                    event.reply_to_msg_id

                if "|" in snip.reply:
                      filter, options= snip.reply.split("|")
                      try:             
                        filter = filter.strip()     
                        button = [options.strip()]
                      except:
                        filter = filters.strip()
                        button = None
                print(f"await event.reply({filter}, buttons={button}, file={media})")
    
                await event.reply(snip.reply, buttons=button, file=media)

                if event.chat_id not in last_triggered_filters:

                    last_triggered_filters[event.chat_id] = []

                last_triggered_filters[event.chat_id].append(name)

                await asyncio.sleep(DELETE_TIMEOUT)

                last_triggered_filters[event.chat_id].remove(name)


@register(pattern="^/savefilter (.*)")
async def on_snip_save(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return

    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()

    if msg:

        snip = {"type": TYPE_TEXT, "text": msg.message or ""}

        if msg.media:

            media = None

            if isinstance(msg.media, types.MessageMediaPhoto):

                media = utils.get_input_photo(msg.media.photo)

                snip["type"] = TYPE_PHOTO

            elif isinstance(msg.media, types.MessageMediaDocument):

                media = utils.get_input_document(msg.media.document)

                snip["type"] = TYPE_DOCUMENT

            if media:

                snip["id"] = media.id

                snip["hash"] = media.access_hash

                snip["fr"] = media.file_reference

        add_filter(
            event.chat_id,
            name,
            snip["text"],
            snip["type"],
            snip.get("id"),
            snip.get("hash"),
            snip.get("fr"),
        )

        await event.reply(f"Filter 
