import time
from julia.events import register
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from pymongo import MongoClient
from julia import MONGO_DB_URI, tbot, OWNER_ID
from julia.events import register
from telethon import types, events
from telethon.tl import functions

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
dbb = client["leccher"]
leechers = dbb.leecher

def max_seconds(max_seconds, *, interval=1):
    interval = int(interval)
    start_time = time.time()
    end_time = start_time + max_seconds
    yield 0
    while time.time() < end_time:
        if interval > 0:
            next_time = start_time
            while next_time < time.time():
                next_time += interval
            time.sleep(int(round(next_time - time.time())))
        yield int(round(time.time() - start_time))
        if int(round(time.time() + interval)) > int(round(end_time)):
            return

global spamcounter
spamcounter=0

@tbot.on(events.NewMessage(pattern=None))
async def leechers(event):
    global spamcounter
    spamcounter += 1
    if str(event.sender_id) in str(OWNER_ID):
      return
    sender = event.sender_id
    senderr = await tbot.get_entity(sender)
    USERSPAM = []
    check = sender
    if len(USERSPAM) >= 1:
        if event.sender_id == USERSPAM[0]:
            pass
        else:
            USERSPAM = []
            USERSPAM.append(check)  
    else:
        USERSPAM = []
        USERSPAM.append(check)  
    for sec in max_seconds(3):
        if spamcounter > 4 and event.sender_id == USERSPAM[0]:
            VALID = True
            spamcounter = 0
            if senderr.username == None:
                st = senderr.first_name
                hh = senderr.id
                final = f"[{st}](tg://user?id={hh}) you are detected as a spammer according to my algorithms.\nYou will be restricted from using any bot commands for 24 hours !"
            else:
                st = senderr.username
                final = f"@{st} you are detected as a spammer according to my algorithms.\nYou will be restricted from using any bot commands for 24 hours !"           
        else:
            VALID = False
            spamcounter = 0
        if VALID == True:
            dev = await event.respond(final)
            users = leechers.find({})
            for c in users:
                if USERSPAM[0] == c["id"]:
                    return
                timerr = time.time()
                leechers.insert_one({"id": USERSPAM[0], "time": timerr})
                try:
                    MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
                    await event.client(
                        EditBannedRequest(event.chat_id, event.sender_id, MUTE_RIGHTS)
                    )
                    await dev.edit(final + "\nYou are now muted !")
                except Exception:
                    pass

# for global spamcheck wrapper



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
 - /setflood <number/off>: set the number of messages to take action on a user for flooding
 - /setfloodmode <mute/ban/kick/tban/tmute>: select the valid action eg. /setfloodmode tmute 5m
 - /flood: gets the current antiflood settings
 - /cleanservice <on/off>: clean telegram's join/left message
 - /cleanbluetext <on/off/yes/no>: clean commands from non-admins after sending
 - /ignorecleanbluetext <word>: prevent auto cleaning of the command
 - /unignorecleanbluetext <word>: remove prevent auto cleaning of the command
 - /listcleanbluetext: list currently whitelisted commands
 - /profanity on/off: filters all explict/abusive words sent by non admins also filters explicit/porn images
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
