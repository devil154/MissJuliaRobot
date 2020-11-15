from julia import tbot
import glob
import os
import subprocess
from telethon import types
from telethon.tl import functions
from julia import tbot
from julia.events import register

from pymongo import MongoClient
from julia import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


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


@register(pattern="^/song (.*)")
async def _(event):
    if event.fwd_from:
        return
    """this method of approve system is made by @AyushChatterjee, god will curse your family if you kang it motherfucker"""
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return

    cmd = event.pattern_match.group(1)
    cmnd = f"{cmd}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    try:
        subprocess.run(["spotdl", "-s", cmnd, "-q", "best"])
        subprocess.run(
            'for f in *.opus; do      mv -- "$f" "${f%.opus}.mp3"; done', shell=True
        )
        l = glob.glob("*.mp3")
        loa = l[0]
        await event.reply("sending the song")
        await tbot.send_file(
            event.chat_id,
            loa,
            force_document=False,
            allow_cache=False,
            supports_streaming=True,
            caption=cmd,
            reply_to=reply_to_id,
        )
        os.system("rm -rf *.mp3")
    except Exception:
        await event.reply("I am getting too many requests !\nPlease try again later.")
from julia import CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
 - /song <songname artist(optional)>: uploads the song in it's best quality available
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
