from julia import tbot
import asyncio
import io
import os
import random
import re
import string

import nltk  
from PIL import Image
from zalgo_text import zalgo

from julia import tbot
from julia.events import register

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

WIDE_MAP = {i: i + 0xFEE0 for i in range(0x21, 0x7F)}
WIDE_MAP[0x20] = 0x3000

from telethon import types, events
from telethon.tl import functions

from pymongo import MongoClient
from julia import MONGO_DB_URI

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


@register(pattern="^/owu$")
async def msg(event):
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
    reply_tex = await event.get_reply_message()
    reply_text = reply_tex.text
    if reply_text is None:
        await event.reply("Reply to a message to make meme.")
        return
    else:
        faces = [
            "(・`ω´・)",
            ";;w;;",
            "owo",
            "UwU",
            ">w<",
            "^w^",
            r"\(^o\) (/o^)/",
            "( ^ _ ^)∠☆",
            "(ô_ô)",
            "~:o",
            ";____;",
            "(*^*)",
            "(>_",
            "(♥_♥)",
            "*(^O^)*",
            "((+_+))",
        ]
        text = re.sub(r"[rl]", "w", reply_text)
        text = re.sub(r"[ｒｌ]", "ｗ", reply_text)
        text = re.sub(r"[RL]", "W", text)
        text = re.sub(r"[ＲＬ]", "Ｗ", text)
        text = re.sub(r"n([aeiouａｅｉｏｕ])", r"ny\1", text)
        text = re.sub(r"ｎ([ａｅｉｏｕ])", r"ｎｙ\1", text)
        text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", text)
        text = re.sub(r"Ｎ([ａｅｉｏｕＡＥＩＯＵ])", r"Ｎｙ\1", text)
        text = re.sub(r"\!+", " " + random.choice(faces), text)
        text = re.sub(r"！+", " " + random.choice(faces), text)
        text = text.replace("ove", "uv")
        text = text.replace("ｏｖｅ", "ｕｖ")
        text += " " + random.choice(faces)
        await event.reply(text)


@register(pattern="^/copypasta$")
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is None:
        await event.reply("Reply to a message tto make meme.")
        return
    else:
        emojis = [
            "😂",
            "😂",
            "👌",
            "✌",
            "💞",
            "👍",
            "👌",
            "💯",
            "🎶",
            "👀",
            "😂",
            "👓",
            "👏",
            "👐",
            "🍕",
            "💥",
            "🍴",
            "💦",
            "💦",
            "🍑",
            "🍆",
            "😩",
            "😏",
            "👉👌",
            "👀",
            "👅",
            "😩",
            "🚰",
        ]
        reply_text = random.choice(emojis)
        b_char = random.choice(rtext).lower()
        for c in rtext:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        await event.reply(reply_text)


@tbot.on(events.NewMessage(pattern="^/bmoji$"))
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is None:
        await event.reply("Reply to a message to make meme.")
        return
    else:
        b_char = random.choice(rtext).lower()
        reply_text = rtext(b_char, "🅱️").replace(
            b_char.upper(), "🅱️"
        )
        await event.reply(reply_text)



@register(pattern="^/clapmoji$")
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is None:
        await event.reply("Reply to a message to make meme.")
        return
    else:
        reply_text = "👏 "
        reply_text += rtext.replace(" ", " 👏 ")
        reply_text += " 👏"
        await event.reply(reply_text)



@tbot.on(events.NewMessage(pattern="^/stretch$"))
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is none:
        await event.reply("Reply to a message to make meme.")
        return
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])", (r"\1" * count), rtext
        )
        await event.reply(reply_text)



@register(pattern="^/vapor(?: |$)(.*)")
async def msg(event):
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
   
    
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext:
        data = rtext
    else:
        data = event.pattern_match.group(1)
    if data is None:
        await event.reply("Either provide some input or reply to a message.")
        return

    reply_text = str(data).translate(WIDE_MAP)
    await event.reply(reply_text)


@register(pattern="^/zalgofy$")
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is none:
        await event.reply("Reply to a message to make meme.")
        return
    else:   
      reply_text = zalgo.zalgo().zalgofy(rtext)
      await event.reply(reply_text)


@register(pattern="^/forbesify$")
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is none:
        await event.reply("Reply to a message to make meme.")
        return
    else:
        data = ""

    data = data.lower()
    accidentals = ["VB", "VBD", "VBG", "VBN"]
    reply_text = data.split()
    offset = 0

    tagged = dict(nltk.pos_tag(reply_text))

    for k in range(len(reply_text)):
        i = reply_text[k + offset]
        if tagged.get(i) in accidentals:
            reply_text.insert(k + offset, "accidentally")
            offset += 1

    reply_text = string.capwords(" ".join(reply_text))
    await event.reply(reply_text)


@register(pattern="^/shout$")
async def msg(event):
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
    rtext = event.pattern_match.group(1)
    
    args = rtext.text
    
    if len(args) == 0:
        await event.reply("Where is text?")
        return

    msg = "```"
    text = " ".join(args)
    result = []
    result.append(" ".join(list(text)))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + " " + "  " * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    await event.reply(msg)


@register(pattern="^/angrymoji$")
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is none:
        await event.reply("Reply to a message to make meme.")
        return
    reply_text = "😡 "
    for i in rtext:
        if i == " ":
            reply_text += " 😡 "
        else:
            reply_text += i
    reply_text += " 😡"
    await event.reply(reply_text)


@register(pattern="^/crymoji$")
async def msg(event):
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
    rtex = await event.get_reply_message()
    rtext = rtex.text
    if rtext is none:
        await event.reply("Reply to a message to make meme.")
        return
    reply_text = "😭 "
    for i in rtext:
        if i == " ":
            reply_text += " 😭 "
        else:
            reply_text += i
    reply_text += " 😭"
    await event.reply(reply_text)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from julia import CHROME_DRIVER
from julia import GOOGLE_CHROME_BIN

CARBONLANG = "en"

@register(pattern="^/carbon (.*)")
async def carbon_api(e):
    """this method of approve system is made by @AyushChatterjee, god will curse your family if you kang it motherfucker"""
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if e.is_group:
        if (await is_register_admin(e.input_chat, e.message.sender_id)):
            pass
        elif e.chat_id == iid and e.sender_id == userss:
            pass
        else:
            return
    

    jj = "`Processing..`"
    gg = await e.reply(jj)
    CARBON = "https://carbon.now.sh/?bg=rgba(239%2C40%2C44%2C1)&t=one-light&wt=none&l=application%2Ftypescript&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=143%25&si=false&es=2x&wm=false&code={code}"
    global CARBONLANG
    code = e.pattern_match.group(1)
    await gg.edit("`Processing..\n25%`")
    os.chdir("./")
    if os.path.isfile("./carbon.png"):
        os.remove("./carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
    driver.get(url)
    await gg.edit("`Processing..\n50%`")
    download_path = "./"
    driver.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_path},
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await gg.edit("`Processing..\n75%`")
    while not os.path.isfile("./carbon.png"):
        await asyncio.sleep(1)
    await gg.edit("`Processing..\n100%`")
    file = "./carbon.png"
    await e.edit("`Uploading..`")
    await tbot.send_file(
        e.chat_id,
        file,
        caption="Made using [Carbon](https://carbon.now.sh/about/),\
        \na project by [Dawn Labs](https://dawnlabs.io/)",
        force_document=True,
    )
    os.remove("./carbon.png")
    driver.quit()

from random import randint, uniform

from PIL import ImageEnhance, ImageOps
from telethon.tl.types import DocumentAttributeFilename

@register(pattern="^/deepfry(?: |$)(.*)")
async def deepfryer(event):
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
    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 1
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await event.reply("`I can't deep fry that!`")
            return
    else:
        await event.reply("`Reply to an image or sticker to deep fry it!`")
        return
    
    image = io.BytesIO()
    await tbot.download_media(data, image)
    image = Image.open(image)
    
    for _ in range(frycount):
        image = await deepfry(image)
    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)
    await event.reply(file=fried_io)


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )
    img = img.copy().convert("RGB")
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageOps.colorize(overlay, colours[0], colours[1])
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))
    return img


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if (
                DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes
            ):
                return False
            if (
                reply_message.gif
                or reply_message.video
                or reply_message.audio
                or reply_message.voice
            ):
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False
    if not data or data is None:
        return False
    else:
        return data

@register(pattern="^/type (.*)")
async def typewriter(typew):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if typew.is_group:
        if await is_register_admin(typew.input_chat, typew.message.sender_id):
            pass
        elif typew.chat_id == iid and typew.sender_id == userss:
            pass
        else:
            return

    message = typew.pattern_match.group(1)
    if message:
        pass
    else:
        await typew.reply("`Give a text to type!`")
        return
    typing_symbol = "|"
    old_text = ""
    now = await typew.reply(typing_symbol)
    await asyncio.sleep(2)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await now.edit(typing_text)
        await asyncio.sleep(2)
        await now.edit(old_text)
        await asyncio.sleep(2)


from julia import CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
**Some memes command, find it all out yourself !**

 - /owo: OWO de text
 - /stretch: STRETCH de text
 - /clapmoji: Type in reply to a message and see magic
 - /bmoji: Type in reply to a message and see magic
 - /copypasta: Type in reply to a message and see magic
 - /vapor: owo vapor dis
 - /shout <text>: Write anything that u want it to should
 - /zalgofy: reply to a message to g̫̞l̼̦i̎͡tͫ͢c̘ͭh̛̗ it out!
 - /table : get flip/unflip :v.
 - /decide : Randomly answers yes/no/maybe
 - /toss : Tosses A coin
 - /abuse : Abuses the cunt
 - /insult : Insult the cunt
 - /slap : Slaps the cunt
 - /roll : Roll a dice.
 - /rlg : Join ears,nose,mouth and create an emo ;-;
 - /react : Check on your own
 - /happy : Check on your own
 - /amgery : Check on your own
 - /cowsay | /tuxsay | /milksay | /kisssay | /wwwsay | /defaultsay | /bunnysay | /moosesay | /sheepsay | /rensay | /cheesesay | /ghostbusterssay | /skeletonsay <text>: Returns a stylish art text from the given text
 - /deepfry: Type this in reply to an image/sticker to roast the image/sticker
 - /figlet: Another Style art
 - /dice: Roll A dice
 - /dart: Throw a dart and try your luck
 - /basketball: Try your luck if you can enter the ball in the ring
 - /type <text>: Make the bot type something for you in a professional way
 - /carbon <text>: Beautifies your text and enwraps inside a terminal image [ENGLISH ONLY]
 - /sticklet <text>: Turn a text into a sticker
 - /fortune: gets a random fortune quote
 - /quotly: Type /quotly in reply to a message to make a sticker of that
 - /animate: Enwrap your text in a beautiful anime
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})

