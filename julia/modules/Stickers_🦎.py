from julia import tbot

from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (
    DocumentAttributeSticker,
    InputStickerSetID,
)

from julia.events import register


@register(pattern="^/packinfo$")
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.reply("Reply to any sticker to get it's pack info.")
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await event.reply("Reply to any sticker to get it's pack info.")
        return
    stickerset_attr_s = rep_msg.document.attributes
    stickerset_attr = find_instance(stickerset_attr_s, DocumentAttributeSticker)
    if not stickerset_attr.stickerset:
        await event.reply("sticker does not belong to a pack.")
        return
    get_stickerset = await tbot(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    await event.reply(
        f"**Sticker Title:** `{get_stickerset.set.title}\n`"
        f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
        f"**Official:** `{get_stickerset.set.official}`\n"
        f"**Archived:** `{get_stickerset.set.archived}`\n"
        f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n"
        f"**Emojis In Pack:** {' '.join(pack_emojis)}"
    )
    
def find_instance(items, class_or_tuple):
    for item in items:
        if isinstance(item, class_or_tuple):
            return item
    return None
    

__help__ = """
 - /packinfo: Reply to a sticker to get it's pack info
 - /getsticker: Uploads the .png of the sticker you've replied to
 - /kang <emoji for sticker>: Reply to a sticker to add it to your pack or makes a new one if it doesn't exist
"""
