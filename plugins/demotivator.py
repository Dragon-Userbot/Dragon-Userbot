from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from .utils.utils import modules_help
import random


@Client.on_message(filters.command(["dem"], ["."]))
async def demotivator(client: Client, message: Message):
    font = requests.get(
        "https://github.com/Dragon-Userbot/files/blob/main/Times%20New%20Roman.ttf?raw=true")
    f = font.content
    template_dem = requests.get(
        "https://raw.githubusercontent.com/Dragon-Userbot/files/main/demotivator.png")
    if message.reply_to_message:
        words = ["random", "text", "typing", "fuck"]
        if message.reply_to_message.photo:
            donwloads = await client.download_media(message.reply_to_message.photo.file_id)
            photo = Image.open(f"{donwloads}")
            resize_photo = photo.resize((469, 312))
            text = message.text.split(" ", maxsplit=1)[1] \
                if len(message.text.split()) > 1 \
                else random.choice(words)
            im = Image.open(BytesIO(template_dem.content))
            im.paste(resize_photo, (65, 48))
            text_font = ImageFont.truetype(BytesIO(f), 22)
            text_draw = ImageDraw.Draw(im)
            text_draw.multiline_text((299, 412),
                                     text,
                                     font=text_font,
                                     fill=(255, 255, 255),
                                     anchor="ms")
            im.save(f"downloads/{message.message_id}.png")
            await message.reply_photo(f"downloads/{message.message_id}.png")
            await message.delete()
        elif message.reply_to_message.sticker:
            if not message.reply_to_message.sticker.is_animated:
                donwloads = await client.download_media(message.reply_to_message.sticker.file_id)
                photo = Image.open(f"{donwloads}")
                resize_photo = photo.resize((469, 312))
                text = message.text.split(" ", maxsplit=1)[1] \
                    if len(message.text.split()) > 1 \
                    else random.choice(words)
                im = Image.open(BytesIO(template_dem.content))
                im.paste(resize_photo, (65, 48))
                text_font = ImageFont.truetype(BytesIO(f), 22)
                text_draw = ImageDraw.Draw(im)
                text_draw.multiline_text((299, 412),
                                         text,
                                         font=text_font,
                                         fill=(255, 255, 255),
                                         anchor="ms")
                im.save(f"downloads/{message.message_id}.png")
                await message.reply_photo(f"downloads/{message.message_id}.png")
                await message.delete()
            else:
                await message.edit("<b>Анимированные стикеры не поддерживаются</b>")
        else:
            await message.edit("<b>Нужно ответить на фото/стикер</b>")
    else:
        await message.edit("<b>Нужно ответить на фото/стикер</b>")
modules_help.update({'demotivator': '''demotivator - Reply to the picture to make a demotivator out of it''', 
                     'demotivator module': 'Demotivator: dem\n'})
