from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests


@Client.on_message(filters.command(["quote"], ["."]) & filters.me)
async def quotes(client: Client, message: Message):
    await message.edit("Цитируем...")
    if message.reply_to_message:
        font = \
            requests.get("https://github.com/Dragon-Userbot/files/blob/main/HelveticaNeue.ttc?raw=true").content
        if message.reply_to_message.text \
            and message.reply_to_message.from_user:
            if message.reply_to_message.from_user.photo:
                a = await client.download_media(message.reply_to_message.from_user.photo.small_file_id)
                avatar = Image.open(f"{a}")
                size = (100, 100)
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                avatar = avatar.resize(size)
                output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                output.thumbnail(size, Image.ANTIALIAS)

                font = ImageFont.truetype(BytesIO(font), 40)
                size = font.getsize(message.reply_to_message.text.markdown)
                size_one = int(str(size).split()[0].split("(")[1].split(",")[0])
                print(size_one)
                size_two = int(str(size).split()[1].split(")")[0])
                y = size_one / 2
                r = str(y).split(".")[0]
                e = int(str(int(r) / 2).split(".")[0])
                print(e)
                if e > 100:
                    im = Image.new("RGBA", (size_one + 55, e), (0, 0, 0, 0))
                else:
                    im = Image.new("RGBA", (size_one + 55, e + 100), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                first_name_font= ImageFont.truetype(BytesIO(font), 30)
                first_name_draw = ImageDraw.Draw(im)
                text_font = ImageFont.truetype(BytesIO(font), 40)
                text_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                 message.reply_to_message.from_user.first_name,
                                 font=first_name_font,
                                 fill=(10, 151, 240))
                text_draw.multiline_text((25, 55),
                                               message.reply_to_message.text,
                                               font=text_font,
                                               fill=(255, 255, 255))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
                await message.reply_to_message.reply_sticker(f"downloads/{message.message_id}.webp")
                await message.delete()


modules_help.update({'mquotes': '''mquote - Reply on user message''',
                     'mquotes module': 'MQuotes: mquote\n'})