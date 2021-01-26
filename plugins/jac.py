from pyrogram import Client, filters
from pyrogram.raw import types, functions
from .utils.utils import modules_help

import requests
from PIL import Image,ImageFont,ImageDraw 
import io
from textwrap import wrap


@Client.on_message(filters.command(['j', 'jac'], ["."]) & filters.me)
def jac(client, message):
    message.delete()
    text = ' '.join(message.command[1:])
    ufr = requests.get("https://github.com/LaciaMemeFrame/FTG-Modules/blob/master/open-sans.ttf?raw=true")
    f = ufr.content
    pic = requests.get("https://raw.githubusercontent.com/LaciaMemeFrame/FTG-Modules/master/jac.jpg")
    pic.raw.decode_content = True
    img = Image.open(io.BytesIO(pic.content)).convert("RGB")
    W, H = img.size
    text = "\n".join(wrap(text, 19))
    t = text + "\n"
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
    w, h = draw.multiline_textsize(t, font=font)
    imtext = Image.new("RGBA", (w+10, h+10), (0, 0,0,0))
    draw = ImageDraw.Draw(imtext)
    draw.multiline_text((10, 10),t,(0,0,0),font=font, align='left')
    imtext.thumbnail((339, 181))
    w, h = 339, 181
    img.paste(imtext, (10,10), imtext)
    out = io.BytesIO()
    out.name = "jac.jpg"
    img.save(out)
    out.seek(0)
    if message.reply_to_message:
        client.send_photo(message.chat.id, out, reply_to_message_id=message.reply_to_message.message_id)
    else:
        client.send_photo(message.chat.id, out)


modules_help.update({'jac': '''<b>Help for |jac|\nUsage:</b>
<code>.jac</code><i>  or</i><code> .j |quote|</code>
<b>[Generate Jacque Fresco quote]</b>
<code>.jac</code><i>  or</i><code> .j</code>
<b>[Reply to the message to generate Jacque Fresco quote]</b>''', 'jac module': '<b>• Jac</b>:<code> .jac </code><i>or</i><code> .j</code>\n'})
