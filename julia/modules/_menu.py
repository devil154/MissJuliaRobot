from julia import CMD_LIST
from julia import tbot
import io
import re
from math import ceil

from telethon import custom, events, Button

from julia.events import register
from julia import CMD_HELP

from telethon import types
from telethon.tl import functions

from pymongo import MongoClient
from julia import MONGO_DB_URI

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
pagenumber = db.pagenumber


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


PM_START_TEXT = """
[Julia](https://telegra.ph/MissJulieRobot-10-24)
"""


@register(pattern="^/start$")
async def start(event):
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

    if not event.is_group:
        await tbot.send_message(event.chat_id, PM_START_TEXT, buttons=[
            [Button.url('Add To Group  👥', 't.me/MissJuliaRobot?startgroup=true'),
             Button.url('Support Group 🎙️', 'https://t.me/MissJuliaRobotSupport')],
            [Button.inline('Commands ❓', data='help_menu'),
                Button.url('Source 📀', 'https://github.com/MissJuliaRobot/MissJuliaRobot')],
            [Button.url('Channel 🗞️', url='https://t.me/MissJuliaRobotNews/2'),
                Button.url('Webiste 🌐', 'missjuliarobot.unaux.com'),
                Button.url('Donate 💲', 'https://ko-fi.com/missjuliarobot')],
            [Button.inline('Close Menu 🔒', f'start_again')]])
    else:
        await event.reply("I am Alive ^_^")


@tbot.on(events.CallbackQuery(pattern=r'start_again'))
async def start_again(event):
    if not event.is_group:
        await event.edit("The menu is closed 🔒", buttons=[
            [Button.inline('Reopen Menu 🔑', f'reopen_again')]])
    else:
        await event.reply("I am Alive ^_^")


@tbot.on(events.CallbackQuery(pattern=r'reopen_again'))
async def reopen_again(event):
    if not event.is_group:
        await event.edit(PM_START_TEXT, buttons=[
            [Button.url('Add To Group  👥', 't.me/MissJuliaRobot?startgroup=true'),
             Button.url('Support Group 🎙️', 'https://t.me/MissJuliaRobotSupport')],
            [Button.inline('Commands ❓', data='help_menu'),
                Button.url('Source 📀', 'https://github.com/MissJuliaRobot/MissJuliaRobot')],
            [Button.url('Channel 🗞️', url='https://t.me/MissJuliaRobotNews/2'),
                Button.url('Webiste 🌐', 'missjuliarobot.unaux.com'),
                Button.url('Donate 💲', 'https://ko-fi.com/missjuliarobot')],
            [Button.inline('Close Menu 🔒', f'start_again')]])
    else:
        await event.reply("I am Alive ^_^")


@register(pattern="^/help$")
async def help(event):
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
    if not event.is_group:
        buttons = paginate_help(event, 0, CMD_LIST, "helpme")
        await event.reply(PM_START_TEXT, buttons=buttons)
    else:
        await event.reply("Contact me in PM to get the help menu", buttons=[
            [Button.url('Help ❓', 't.me/MissJuliaRobot?start=help')]])


@register(pattern="^/start help$")
async def help(event):
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
    if not event.is_group:
        buttons = paginate_help(event, 0, CMD_LIST, "helpme")
        await event.reply(PM_START_TEXT, buttons=buttons)
    else:
        await event.reply("Contact me in PM to get the help menu", buttons=[
            [Button.url('Help ❓', 't.me/MissJuliaRobot?start=help')]])


@tbot.on(events.CallbackQuery(pattern=r'help_menu'))
async def help_menu(event):
    buttons = paginate_help(event, 0, CMD_LIST, "helpme")
    await event.edit(PM_START_TEXT, buttons=buttons)


@tbot.on(
    events.callbackquery.CallbackQuery(
        data=re.compile(rb"helpme_next\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = paginate_help(event, current_page_number + 1, CMD_LIST, "helpme")
    await event.edit(buttons=buttons)


@tbot.on(
    events.callbackquery.CallbackQuery(
        data=re.compile(rb"helpme_prev\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    current_page_number = int(event.data_match.group(1).decode("UTF-8"))
    buttons = paginate_help(event,
                            current_page_number - 1, CMD_LIST, "helpme"
                            )
    await event.edit(buttons=buttons)


@tbot.on(
    events.callbackquery.CallbackQuery(
        data=re.compile(b"us_plugin_(.*)")
    )
)
async def on_plug_in_callback_query_handler(event):
    plugin_name = event.data_match.group(1).decode("UTF-8")
    help_string = ""
    # By @MissJuliaBeta_Robot

    for i in CMD_LIST[plugin_name]:
        plugin = plugin_name.replace("_", " ")
        emoji = plugin_name.split("_")[0]
        output = str(CMD_HELP[plugin][1])
        help_string = f"Here is the help for **{emoji}**:\n" + output

    if help_string is None:
        pass  # stuck on click
    else:
        reply_pop_up_alert = help_string
    try:
        await event.edit(reply_pop_up_alert, buttons=[
            [Button.inline('🔙 Back', f'go_back')]])
    except BaseException:
        with io.BytesIO(str.encode(reply_pop_up_alert)) as out_file:
            out_file.name = "{}.txt".format(plugin_name)
            await tbot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=plugin_name,
            )


@tbot.on(events.CallbackQuery(pattern=r'go_back'))
async def go_back(event):
    c = pagenumber.find_one({"id": event.sender_id})
    number = c["page"]
    # print (number)
    buttons = paginate_help(event, number, CMD_LIST, "helpme")
    await event.edit(PM_START_TEXT, buttons=buttons)


def get_page(id):
    return pagenumber.find_one({'id': id})


def paginate_help(event, page_number, loaded_plugins, prefix):
    number_of_rows = 3
    number_of_cols = 2
    sender = event.sender_id
    #  print (page_number)

    to_check = get_page(id=event.sender_id)

    if not to_check:
        pagenumber.insert_one({'id': event.sender_id, 'page': page_number})

    else:
        pagenumber.update_one(
            {
                '_id': to_check["_id"],
                'id': to_check["id"],
                'page': to_check["page"],
            }, {"$set": {
                'page': page_number
            }})

    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{}".format(x.replace("_", " ")), data="us_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⏮️", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline("⏹️", data='reopen_again'),
                custom.Button.inline(
                    "⏭️", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs
