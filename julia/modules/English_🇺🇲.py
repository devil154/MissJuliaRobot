from julia import tbot
import json
import requests
from emoji import UNICODE_EMOJI
from googletrans import Translator
from telegram.ext import CommandHandler
from telegram.ext import run_async
from julia import CMD_HELP, MONGO_DB_URI
from julia.events import register
from telethon import *
from telethon.tl import functions
from pymongo import MongoClient
import os, subprocess

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["test"]
approved_users = db.approve

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await
             tbot(functions.channels.GetParticipantRequest(chat,
                                                           user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (await tbot(functions.messages.GetFullChatRequest(chat.chat_id)
                         )).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


@register(pattern="^/tr (.*)")
async def _(event):
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
    lang = event.pattern_match.group(1)
    if not lang:
        lang = "en"
    thetext = await event.get_reply_message()
    translate_text = thetext.text
    ignore_text = UNICODE_EMOJI.keys()
    for emoji in ignore_text:
        if emoji in translate_text:
            translate_text = translate_text.replace(emoji, "")

    translator = Translator()
    try:
        translated = translator.translate(translate_text, dest=lang)
        trl = translated.src
        results = translated.text
        await event.reply("Translated from {} to {}.\n {}".format(trl, lang, results))
    except BaseException:
        await event.reply("Error! invalid language code.")


API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
URL = "http://services.gingersoftware.com/Ginger/correct/json/GingerTheText"


@register(pattern="^/spell(?: |$)(.*)")
async def _(event):
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
    ctext = await event.get_reply_message()
    msg = ctext.text
    print (msg)
    params = dict(lang="US", clientVersion="2.0", apiKey=API_KEY, text=msg)

    res = requests.get(URL, params=params)
    changes = json.loads(res.text).get("LightGingerTheTextResult")
    curr_string = ""
    prev_end = 0

    for change in changes:
            start = change.get("From")
            end = change.get("To") + 1
            suggestions = change.get("Suggestions")
            if suggestions:
                sugg_str = suggestions[0].get("Text")
                curr_string += msg[prev_end:start] + sugg_str
                prev_end = end

            curr_string += msg[prev_end:]
            await event.reply(curr_string)


import inspect
import logging
import re, os
from pathlib import Path
from julia import tbot, CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")


__help__ = """
 - /spell: while replying to a message, will reply with a grammar corrected version
 - /forbesify: Correct your punctuations better use the advanged spell module
 - /tr (language code) as reply to a long message.
 - /define <text>: Type the word or expression you want to search\nFor example /define Gay
 - /emotion: Type in reply to a message to check emotions 
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
