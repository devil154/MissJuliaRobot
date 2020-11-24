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
from contextlib import contextmanager
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

from julia import **

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


# ------ THANKS TO LONAMI ------#
async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (await
             tbot(functions.channels.GetParticipantRequest(chat,
                                                           user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    elif isinstance(chat, types.InputPeerChat):
        ui = await tbot.get_peer_id(user)
        ps = (await tbot(functions.messages.GetFullChatRequest(chat.chat_id)
                         )).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    else:
        return None
        
@register(pattern="^/git")
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
    text = event.text[len("/git "):]
    usr = get(f"https://api.github.com/users/{text}").json()
    if usr.get("login"):
        reply_text = f"""**Name:** `{usr['name']}`
        **Username:** `{usr['login']}`
        **Account ID:** `{usr['id']}`
        **Account type:** `{usr['type']}`
        **Location:** `{usr['location']}`
        **Bio:** `{usr['bio']}`
        **Followers:** `{usr['followers']}`
        **Following:** `{usr['following']}`
        **Hireable:** `{usr['hireable']}`
        **Public Repos:** `{usr['public_repos']}`
        **Public Gists:** `{usr['public_gists']}`
        **Email:** `{usr['email']}`
        **Company:** `{usr['company']}`         
        **Website:** `{usr['blog']}`
        **Last updated:** `{usr['updated_at']}`
        **Account created at:** `{usr['created_at']}`
        """
    else:
        reply_text = "User not found. Make sure you entered valid username!"
    await event.reply(reply_text)



@register(pattern="^/repo")
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
    text = event.text[len("/repo "):]
    usr = get(f"https://api.github.com/users/{text}/repos?per_page=300").json()
    reply_text = "**Repo**\n"
    for i in range(len(usr)):
        reply_text += f"[{usr[i]['name']}]({usr[i]['html_url']})\n"
    await event.reply(reply_text, link_preview=False)
