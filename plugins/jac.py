from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw import types, functions
from .utils.utils import modules_help

import requests
from PIL import Image, ImageFont, ImageDraw
import io
from textwrap import wrap


@Client.on_message(filters.command(['j', 'jac'], ["."]) & filters.me)
async def jac(client: Client, message: Message):
    if message.command[1:]:
        text = ' '.join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = ' '
    await message.delete()
    ufr = requests.get(
        "https://github.com/Dragon-Userbot/files/blob/main/CascadiaCodePL.ttf?raw=true")
    f = ufr.content
    pic = requests.get(
        "https://raw.githubusercontent.com/Dragon-Userbot/files/main/jac.jpg")
    pic.raw.decode_content = True
    img = Image.open(io.BytesIO(pic.content)).convert("RGB")
    W, H = img.size
    text = "\n".join(wrap(text, 19))
    t = text + "\n"
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
    w, h = draw.multiline_textsize(t, font=font)
    imtext = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(imtext)
    draw.multiline_text((10, 10), t, (0, 0, 0), font=font, align='left')
    imtext.thumbnail((339, 181))
    w, h = 339, 181
    img.paste(imtext, (10, 10), imtext)
    out = io.BytesIO()
    out.name = "jac.jpg"
    img.save(out)
    out.seek(0)
    if message.reply_to_message:
        await client.send_photo(message.chat.id, out, reply_to_message_id=message.reply_to_message.message_id)
    else:
        await client.send_photo(message.chat.id, out)


modules_help.update({'jac': '''jac |quote| - Generate Jacque Fresco quote, jac - Reply to the message to generate Jacque Fresco quote''',
                     'jac module': 'Jac: jac'})
