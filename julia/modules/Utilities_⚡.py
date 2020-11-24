import io
import sys
import traceback, random, time
from time import sleep
import pyfiglet
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
from telethon.errors import *
from julia import *

from julia import StartTime
from julia.events import register, juliabot

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

import os
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from julia import CMD_HELP
from julia.events import register

TMP_DOWNLOAD_DIRECTORY = "./"


@register(pattern="^/info(?: |$)(.*)")
async def who(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender.id == userss:
            pass
        else:
            return
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    caption = await fetch_info(replied_user, event)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    await event.reply(caption, parse_mode="html")


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await tbot(
            GetFullUserRequest(previous_message.sender_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await tbot.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await tbot(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await tbot.get_entity(user)
            replied_user = await tbot(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    first_name = first_name.replace(
        "\u2060", "") if first_name else ("This User has no First Name")
    last_name = last_name.replace(
        "\u2060", "") if last_name else ("This User has no Last Name")
    username = "@{}".format(username) if username else (
        "This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio

    if user_id != (await tbot.get_me()).id:
        common_chat = replied_user.common_chats_count
    else:
        common_chat = "I've seen them in... Wow. Are they stalking me? "
        common_chat += "They're in all the same places I am... oh. It's me."

    caption = "<b>USER INFO:</b> \n"
    caption += f"First Name: {first_name} \n"
    caption += f"Last Name: {last_name} \n"
    caption += f"Username: {username} \n"
    caption += f"Is Bot: {is_bot} \n"
    caption += f"Is Restricted: {restricted} \n"
    caption += f"Is Verified by Telegram: {verified} \n"
    caption += f"ID: <code>{user_id}</code> \n \n"
    caption += f"Bio: \n<code>{user_bio}</code> \n \n"
    caption += f"Common Chats with this user: {common_chat} \n\n"
    caption += f"Permanent Link To Profile: "
    caption += f"<a href=\"tg://user?id={user_id}\">{first_name}</a>"

    if user_id in SUDO_USERS:
         caption += f"\n\n<b>This person is one of my SUDO USERS\nHe can Gban/Ungban anyome, so mind it !</b>"
    
    if user_id == OWNER_ID:
         caption += f"\n\n<b>This person is my owner.\nHe is the reason why I am alive.</b>"

    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
  
    if event.chat_id == iid and event.sender_id == userss:
       caption += f"\n\n<b>This person is approved in this chat.</b>"

    return caption

@register(pattern="^/userid$")
async def useridgetter(target):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if target.is_group:
        if await is_register_admin(target.input_chat, target.message.sender_id):
            pass
        elif target.chat_id == iid and target.sender_id == userss:
            pass
        else:
            return
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"

        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.reply("**Name:** {} \n**User ID:** `{}`".format(
            name, user_id))


@register(pattern="^/chatid$")
async def chatidgetter(chat):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if chat.is_group:
        if await is_register_admin(chat.input_chat, chat.message.sender_id):
            pass
        elif chat.chat_id == iid and chat.sender_id == userss:
            pass
        else:
            return
    await chat.reply("Chat ID: `" + str(chat.chat_id) + "`")

@register(pattern="^/runs$")
async def runs(event):
    RUNIT = [
        "Now you see me, now you don't.",
        "ε=ε=ε=ε=┌(;￣▽￣)┘",
        "Get back here!",
        "REEEEEEEEEEEEEEEEEE!!!!!!!",
        "Look out for the wall!",
        "Don't leave me alone with them!!",
        "You've got company!",
        "Chotto matte!",
        "Yare yare daze",
        "*Naruto run activated*",
        "*Nezuko run activated*",
        "Hey take responsibilty for what you just did!",
        "May the odds be ever in your favour.",
        "Run everyone, they just dropped a bomb 💣💣",
        "And they disappeared forever, never to be seen again.",
        "Legend has it, they're still running.",
        "Hasta la vista, baby.",
        "Ah, what a waste. I liked that one.",
        "As The Doctor would say... RUN!",
    ]
    await event.reply(random.choice(RUNIT))



def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


@register(pattern="^/ping$")
async def ping(event):
    import datetime
    start_time = datetime.datetime.now()
    message = await event.reply("Pinging .")
    await message.edit("Pinging ..")
    await message.edit("Pinging ...")
    end_time = datetime.datetime.now()
    pingtime = end_time - start_time
    telegram_ping = str(round(pingtime.total_seconds(), 2)) +"s"    
    uptime = get_readable_time((time.time() - StartTime))
    await message.edit(
        "PONG !\n"
        "<b>Time Taken:</b> <code>{}</code>\n"
        "<b>Service uptime:</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode="html",
    )

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
    return await locals()["__aexec"](message, reply, tbot, p)


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

@juliabot(pattern="/saved")
async def saat(event):
    chat = "@FileToLinkTGbot"
    async with event.client.conversation(chat) as conv:
        try:
            response = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=1011636686))
            await reply_message.forward_to(chat, debloat)
            response = await response
        except YouBlockedUserError:
            return
        if not response:
            return
        if response.text.startswith("🔗"):
            #    my_string= response.text
            #    p = re.compile(":(.*)")
            #    global holababy
            #    holababy = p.findall(my_string)
            global holababy
            holababy = response.text


@register(pattern="^/savefile$")
async def savel(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    global reply_message
    reply_message = await event.get_reply_message()
    entity = await event.client.get_entity(OWNER_USERNAME)
    randika = await event.client.send_message(entity, "/saved")
    await event.reply(f"{holababy}")
    await randika.delete()
    del holababy
    del reply_message
    

from julia import CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
 - /userid: If replied to user's message gets that user's id.
 - /chatid: Get the current chat id. 
 - /runs: Reply a random string from an array of replies.
 - /info: Get information about a user.
 - /savefile: Gives you a permanent link of a file so that you can download it later anytime
"""
CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
