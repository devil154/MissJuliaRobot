from julia import tbot, CMD_HELP
from pathlib import Path
import logging
import inspect
import asyncio
import glob
import html
import io
import json
import os
import random
import re
import subprocess
import sys
import textwrap
import time
import traceback
import urllib.request
from datetime import datetime
from html import unescape
from random import randrange
from time import sleep
from typing import List
from typing import Optional
from urllib.request import urlopen

import aiohttp
import barcode
import bs4
import emoji
import html2text
import nude
import pyfiglet
import requests
import telegraph
import text2emotion as machi
from barcode.writer import ImageWriter
from better_profanity import profanity
from bing_image_downloader import downloader
from cowpy import cow
from fontTools.ttLib import TTFont
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gtts import gTTS
from gtts import gTTSError
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from PyDictionary import PyDictionary
from pymongo import MongoClient
from requests import get
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Message
from telegram import MessageEntity
from telegram import ParseMode
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import run_async
from telegram.utils.helpers import escape_markdown
from telegram.utils.helpers import mention_html
from telegraph import Telegraph
from telethon import *
from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.errors import FloodWaitError
from telethon.errors import UserAdminInvalidError
from telethon.errors import YouBlockedUserError
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import *
from tswift import Song
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError
from wikipedia.exceptions import PageError

from julia import *
from julia.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve

# ------ THANKS TO LONAMI ------#


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
    return False


@register(pattern="^/stt$")
async def _(event):
    if event.fwd_from:
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
    start = datetime.now()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await event.client.download_media(
            previous_message, TEMP_DOWNLOAD_DIRECTORY
        )
        if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
            await event.reply(
                "You need to set the required ENV variables for this module. \nModule stopping"
            )
        else:
            await event.reply("Starting analysis")
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", IBM_WATSON_CRED_PASSWORD),
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + \
                        str(alternatives["transcript"])
                    transcript_confidence += (
                        " " + str(alternatives["confidence"]) + " + "
                    )
                end = datetime.now()
                ms = (end - start).seconds
                if transcript_response != "":
                    string_to_show = "Language: `English`\nTRANSCRIPT: `{}`\nTime Taken: {} seconds\nConfidence: `{}`".format(
                        transcript_response, ms, transcript_confidence)
                else:
                    string_to_show = "Language: `English`\nTime Taken: {} seconds\n**No Results Found**".format(
                        ms)
                await event.reply(string_to_show)
            else:
                await event.reply(r["error"])
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await event.reply("Reply to a voice message, to get the text out of it.")

global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /stt: Type in reply to a voice message(english only) to extract text from it.
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
