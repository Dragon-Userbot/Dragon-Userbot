from pyrogram import Client, filters
from .utils.utils import modules_help

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import time

def drawtext(text, text_color, background_color):
    global tg_img
    font_size = 20
    font = ImageFont.truetype("plugins/utils/CascadiaCodePL.ttf", font_size)
    width = font.getsize(max(text.split('\n'), key=len))[0] + 35
    height = font.getsize(text.split('\n')[0])[1] * text.count('\n') + 40
    img = Image.new('RGB', (width, height), color=f'{background_color}')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=font, fill=f'{text_color}')

    tg_img = BytesIO()
    tg_img.name = 'tg.png'
    img.save(tg_img, 'PNG')
    tg_img.seek(0)
    return tg_img

@Client.on_message(filters.command('tti', ['.']) & filters.me)
def text_to_img(client, message):
    global tg_img
    text_color = message.command[1]
    background_color = message.command[2]
    text = ' '.join(message.command[3:])

    if text == '':
        if message.reply_to_message:
            message.delete()
            text = message.reply_to_message.text
            drawtext(text, text_color, background_color)
            client.send_photo(message.chat.id, tg_img, reply_to_message_id=message.reply_to_message.message_id)
    else:
        message.delete()
        drawtext(text, text_color, background_color)
        if message.reply_to_message == None:
            client.send_photo(message.chat.id, tg_img)
        else:
            client.send_photo(message.chat.id, tg_img, reply_to_message_id=message.reply_to_message.message_id)


modules_help.update({'text2img': '''<b>Help for |text2img|\nUsage:</b>
<code>.tti [text color] [background color] [text]</code>
<b>[Simple color names or hex!]</b>
<b>[Turning text into a picture]</b>''', 'text2img module': '<b>• Text2img</b>:<code> tti</code>\n'})

requirements_list.append('pillow')
