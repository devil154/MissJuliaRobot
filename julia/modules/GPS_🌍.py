from geopy.geocoders import Nominatim
from julia.events import register
from julia import *
from telethon import *
from telethon.tl import *
from pymongo import MongoClient

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

GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"

@register(pattern="^/gps (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
 
    try:
        geolocator = Nominatim(user_agent="SkittBot")
        location = args
        geoloc = geolocator.geocode(location)
        longitude = geoloc.longitude
        latitude = geoloc.latitude
        gm = "https://www.google.com/maps/search/{},{}".format(lat, lon)
        await tbot.send_file(event.chat_id, file=types.InputMediaGeoPoint(types.InputGeoPoint(float(latitude), float(longitude))))
        await event.reply(
            "Open with: [Google Maps]({})".format(gm),
            link_preview=False,
        )
    except AttributeError:
        await event.reply("I can't find that")

import os
from julia import tbot, CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
 - /gps: <location> Get gps location.
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
