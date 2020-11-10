import io
import sys
import traceback

import pyfiglet
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from julia import *

from julia.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["test"]
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


@register(pattern="^/figlet (.*)")
async def figlet(event):
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.from_id == userss:
            pass
        else:
            return
    input_str = event.pattern_match.group(1)
    result = pyfiglet.figlet_format(input_str)
    await event.respond("`{}`".format(result))


@register(pattern="^/eval")
async def _(event):
    check = event.message.sender_id
    checkint = int(check)
    if int(check) != int(OWNER_ID):
        return
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success 😃"

    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )

    else:
        await event.reply(final_output)


async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(slitu.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, reply, client, p): "
        + "\n event = smessatatus = message"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](message, reply, message.client, p)


@juliabot(pattern=".eval")
async def _(event):
    check = event.message.sender_id
    checkint = int(check)
    # print(checkint)
    if int(check) != int(OWNER_ID):
        return
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success 😃"

    final_output = "**OUTPUT**:\n\n`{}`".format(evaluation)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await ubot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )

    else:
        await event.reply(final_output)



__help__ = """
 - /id: get the current group id. If replied to user's message gets that user's id.
 - /runs: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /info: get information about a user.
 - /paste: Create a paste or a shortened url using del.dog
 - /getpaste: Get the content of a paste or shortened url from del.dog
 - /pastestats: Get stats of a paste or shortened url from del.dog
 - /removebotkeyboard: Got a nasty bot keyboard stuck in your group?
 - /shrug: try and check it out yourself.
 - /datetime <city>: Get the present date and time information
 - /camscanner: Reply to a image to scan and improve it's clarity.
*Instructions*
▪️The image should be a page with some written text on it (screenshots aren't permitted)
▪️The image should contain the page with four corners clearly visible
▪️The background should be somewhat darker than the page
▪️The image should contain only the page with no other objects like pencil, eraser etc. beside it(within the image)
*PRO TIP*
You can simply draw a border(a black square) around the portion you want to scan for better efficiency and edge detection
If you are still messed up send `/helpcamscanner` in pm for the tutorial !
 - /google <text>: perform a google search
 - /gps: <location> Get gps location.
 - /imdb - Get full info about a movie with imdb.com
 - /img <text>: Search Google for images and returns them\nFor greater no. of results specify lim, For eg: `/img hello lim=10`
 - /img2text <lang>: Type in reply to a image to extract the text from it
 - /img2textlang: List all the available languages
 - /phone <number in international format>: Check if the number really exists and returns information about it.If the number is fake then it will return null-type response
Example: `/phone +9162XX93X805`, `/phone +1916X978XX1`
 - /news: Returns today's Indian Headlines (ONLY WORKS IN PM)
 - /getqr: Get the QR Code content from the replied QR Code
 - /makeqr <content>: Make a QR Code from the given message (text, link, etc...)
 - /reverse: Does a reverse image search of the media which it was replied to.
 - /rmbg: Type in reply to a media to remove it's background
 - /stt: Type in reply to a voice message(english only) to extract text from it.
 - /tts <lang | text>: Returns a speech note of the text provided
 - /torrent <text>: Search for torrent links
If you are still messed up send `/helptorrent` in pm for the tutorial !
 - /wall <topic>: Searches best wallpaper on the given topic and returns them
 - /weather <city>: Get weather info in a particular place
 - /wttr <city>: Advanced weather module, usage same as /weather
 - /wttr moon: Get the current status of moon
 - /wiki <text>: Returns search from wikipedia for the input text
 - /yt <text>: perform a youtube search
 - /ytaudio <link> or /ytvideo <link>: Downlods a video or audio from a youtube video to the bots local server
 - /zip: reply to a telegram file to compressing in .zip format
 - /unzip: reply to a telegram file to decompress it from the .zip format
 - /git <username>: Returns info about a GitHub user or organization.
 - /repo <username>: Return the GitHub user or organization repository list
 - /app <appname>: Search for an app in playstore
 - /magisk: Get the latest Magisk releases
 - /device <codename>: Get info about an Android device
 - /codename <brand> <device>: Search for Android device codename
 - /specs <brand> <device>: Get device specifications info
 - /twrp <codename>: Get the latest TWRP download for an Android device
 - /song <songname artist(optional)>: uploads the song in it's best quality available
 - /lyrics <songname artist (optional)>: get the lyrics of a song
 - /barcode <text>: makes a barcode out of the text, crop the barcode if you don't want to reveal the text
 - /savefile: Gives you a permanent link of a file so that you can download it later anytime
"""

