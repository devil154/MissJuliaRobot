from translate import Translator 
from julia import tbot
import json
import requests
from julia import CMD_HELP, MONGO_DB_URI
from julia.events import register
from telethon import *
from telethon.tl import functions
from pymongo import MongoClient
import os
import random
import re
import time
import urllib.request
from typing import List
from typing import Optional

import aiohttp
import bs4
import text2emotion as machi
from better_profanity import profanity
from cowpy import cow
from PyDictionary import PyDictionary
from telegram import Message
from telegram import MessageEntity
from telethon.errors import ChatAdminRequiredError
from telethon.errors import UserAdminInvalidError
from telethon.tl import types
from telethon.tl.types import *
from tswift import Song



client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
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
    thetext = await event.get_reply_message()
    translate_text = thetext.text
    translator= Translator(to_lang=lang)
    translation = translator.translate(translate_text)
    await event.reply(translation)
    

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
    #  print (msg)
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


dictionary = PyDictionary()


@register(pattern="^/define")
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
    text = event.text[len("/define "):]
    word = f"{text}"
    let = dictionary.meaning(word)
    set = str(let)
    jet = set.replace("{", "")
    net = jet.replace("}", "")
    got = net.replace("'", "")
    await event.reply(got)


@register(pattern="^/synonyms")
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
    text = event.text[len("/synonyms "):]
    word = f"{text}"
    let = dictionary.synonym(word)
    set = str(let)
    jet = set.replace("{", "")
    net = jet.replace("}", "")
    got = net.replace("'", "")
    await event.reply(got)


@register(pattern="^/antonyms")
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
    text = message.text[len("/antonyms "):]
    word = f"{text}"
    let = dictionary.antonym(word)
    set = str(let)
    jet = set.replace("{", "")
    net = jet.replace("}", "")
    got = net.replace("'", "")
    await event.reply(got)

@register(pattern="^/emotion$")
async def _(event):
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

    reply = await event.get_reply_message()
    msg = reply.message
    let = str(machi.get_emotion(msg))
    # m = let.replace("'Happy'", "😀")
    n = let.replace("{", "")
    o = n.replace("}", "")
    # p = o.replace("'Angry'", "😡")
    # q = p.replace("'Sad'", "😭")
    # r = q.replace("'Surprise'", "😮")
    # s = r.replace("'Fear'", "")
    t = o.replace(", ", "\n\n")
    await event.reply(t)


import inspect
import logging
from pathlib import Path
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")


__help__ = """
 - /spell: while replying to a message, will reply with a grammar corrected version
 - /forbesify: Correct your punctuations better use the advanged spell module
 - /tr <language code>: Type in reply to a message to get it's translation in the destination language
 - /define <text>: Type the word or expression you want to search\nFor example /define Gay
 - /emotion: Type in reply to a message to check emotions 
 - /synonyms <word>: Find the synonyms of a word 
 - /antonyms <word>: Find the antonyms of a word 
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
