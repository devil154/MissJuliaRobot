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


telegraph = Telegraph()
telegraph.create_account(short_name="Julia")


@register(pattern="^/torrent (.*)")
async def tor_search(event):
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
    str = event.pattern_match.group(1)
    let = f'"{str}"'
    jit = subprocess.check_output(["we-get", "-s", let, "-t", "all", "-J"])
    proc = jit.decode()
    sit = proc.replace("{", "")
    pit = sit.replace("}", "")
    op = pit.replace(",", "")
    seta = f"Magnets for {str} are below:"
    response = telegraph.create_page(seta, html_content=op)
    await event.reply(
        "Magnet Links for {}:\n\nhttps://telegra.ph/{}".format(str, response["path"]),
        link_preview=False,
    )
   
   
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
 - /torrent <text>: Search for torrent links
If you are still messed up send `/helptorrent` in pm for the tutorial !
"""
CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})

