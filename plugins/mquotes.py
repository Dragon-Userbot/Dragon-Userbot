from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests


@Client.on_message(filters.command(["mquote", "mq"], ["."]) & filters.me)
async def quotes(client: Client, message: Message):
    await message.edit("<code>Quoting ...</code>")
    if message.reply_to_message:
        font = requests.get(
            "https://github.com/Dragon-Userbot/files/blob/main/HelveticaNeue.ttc?raw=true")
        f = font.content
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
            else:
                avatar = Image.new('RGBA', (100, 100), (255, 202, 144, 1))
                size = (100, 100)
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                avatar = avatar.resize(size)
                output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                output.thumbnail(size, Image.ANTIALIAS)
                avater_text_font = ImageFont.truetype(BytesIO(f), 40)
                avatar_text_draw = ImageDraw.Draw(output)
                avatar_text_draw.multiline_text((35, 25), list(message.reply_to_message.from_user.first_name)[0],
                                                font=avater_text_font,
                                                fill=(255, 255, 255))
            try:
                reply_msg = await client.get_messages(message.chat.id,
                                                      reply_to_message_ids=message.reply_to_message.message_id)
                count = 0
                text = ""
                for _ in message.reply_to_message.text.split():
                    if count != 9:
                        text += f" {_}"
                        count += 1
                    else:
                        count = 0
                        text += f"\n{_}"
                font_test = ImageFont.truetype(BytesIO(f), 40)
                list_size = []
                for _ in text.split("\n"):
                    ize = font_test.getsize(_)
                    list_size.append(int(str(ize).split()[0].split("(")[1].split(",")[0]))
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.from_user.first_name)
                reply_first_name_font = ImageFont.truetype(BytesIO(f), 25)
                reply_text_font = ImageFont.truetype(BytesIO(f), 35)
                if reply_msg.from_user:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.from_user.first_name)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.from_user.first_name
                elif reply_msg.sender_chat:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.sender_chat.title)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.sender_chat.title
                if reply_msg.text:
                    if len(list(reply_msg.text)) > 15:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = font_name.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                    else:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = reply_text_font.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.document:
                    msg = "Document"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.photo:
                    msg = "Photo"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.animation:
                    msg = "GIF"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.voice:
                    msg = "Voice"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.audio:
                    msg = "Audio"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.sticker:
                    msg = "Sticker"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                else:
                    msg = "Unsupported type"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                width = max(list_size) + int(str(size_name).split()[0].split("(")[1].split(",")[0]) + int(((size_rep_name + reply_tex_size) / 2))
                tab = 50 * (len(text.split("\n")) + 1)
                im = Image.new("RGBA", (width + 40, tab + 150), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                draw.line((25, 50, 25, 155), fill=(255, 255, 255), width=4)

                reply_first_name_draw = ImageDraw.Draw(im)
                reply_text_draw = ImageDraw.Draw(im)
                reply_first_name_draw.multiline_text((40, 60),
                                                name,
                                                font=reply_first_name_font,
                                                fill=(10, 151, 240))
                reply_text_draw.multiline_text((40, 90),
                                            msg,
                                            font=reply_text_font,
                                            fill=(255, 255, 255))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                text_font = ImageFont.truetype(BytesIO(f), 40)
                text_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.from_user.first_name,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                text_draw.multiline_text((25, 165),
                                         text,
                                         font=text_font,
                                         fill=(255, 255, 255))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
            except:
                count = 0
                text = ""
                for _ in message.reply_to_message.text.split():
                    if count != 9:
                        text += f" {_}"
                        count += 1
                    else:
                        count = 0
                        text += f"\n{_}"
                font_test = ImageFont.truetype(BytesIO(f), 40)
                list_size = []
                for _ in text.split("\n"):
                    ize = font_test.getsize(_)
                    list_size.append(int(str(ize).split()[0].split("(")[1].split(",")[0]))
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.from_user.first_name)
                width = max(list_size) + int(str(size_name).split()[0].split("(")[1].split(",")[0])
                tab = 50 * (len(text.split("\n")) + 1)
                im = Image.new("RGBA", (width + 40, tab + 40), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                text_font = ImageFont.truetype(BytesIO(f), 40)
                text_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.from_user.first_name,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                text_draw.multiline_text((25, 55),
                                         text,
                                         font=text_font,
                                         fill=(255, 255, 255))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
            await message.reply_to_message.reply_document(f"downloads/{message.message_id}.webp")
            await message.delete()

        if not message.reply_to_message.text \
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
            else:
                avatar = Image.new('RGBA', (100, 100), (255, 202, 144, 1))
                size = (100, 100)
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                avatar = avatar.resize(size)
                output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                output.thumbnail(size, Image.ANTIALIAS)
                avater_text_font = ImageFont.truetype(BytesIO(f), 40)
                avatar_text_draw = ImageDraw.Draw(output)
                avatar_text_draw.multiline_text((35, 25), list(message.reply_to_message.from_user.first_name)[0],
                                                font=avater_text_font,
                                                fill=(255, 255, 255))
            try:
                reply_msg = await client.get_messages(message.chat.id,
                                                      reply_to_message_ids=message.reply_to_message.message_id)
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.from_user.first_name)
                reply_first_name_font = ImageFont.truetype(BytesIO(f), 25)
                reply_text_font = ImageFont.truetype(BytesIO(f), 35)
                if reply_msg.from_user:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.from_user.first_name)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.from_user.first_name
                elif reply_msg.sender_chat:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.sender_chat.title)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.sender_chat.title
                if reply_msg.text:
                    if len(list(reply_msg.text)) > 15:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = font_name.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                    else:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = reply_text_font.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.document:
                    msg = "Document"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.photo:
                    msg = "Photo"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.animation:
                    msg = "GIF"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.voice:
                    msg = "Voice"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.audio:
                    msg = "Audio"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.sticker:
                    msg = "Sticker"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                else:
                    msg = "Unsupported type"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                y_n = int(str(size_name).split()[1].split(")")[0])
                width = int(str(size_name).split()[0].split("(")[1].split(",")[0]) + int(
                    (size_rep_name + reply_tex_size) + ((size_rep_name + reply_tex_size) / 2))
                im = Image.new("RGBA", (width + 40, y_n + 150), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                draw.line((25, 50, 25, 155), fill=(255, 255, 255), width=4)

                reply_first_name_draw = ImageDraw.Draw(im)
                reply_text_draw = ImageDraw.Draw(im)
                reply_first_name_draw.multiline_text((40, 60),
                                                     name,
                                                     font=reply_first_name_font,
                                                     fill=(10, 151, 240))
                reply_text_draw.multiline_text((40, 90),
                                               msg,
                                               font=reply_text_font,
                                               fill=(255, 255, 255))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.from_user.first_name,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
                await message.reply_to_message.reply_document(f"downloads/{message.message_id}.webp")
                await message.delete()
            except:
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.from_user.first_name)
                x_n = int(str(size_name).split()[0].split("(")[1].split(",")[0])
                y_n = int(str(size_name).split()[1].split(")")[0])
                im = Image.new("RGBA", (x_n + 100, y_n + 100), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.from_user.first_name,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
                await message.reply_to_message.reply_document(f"downloads/{message.message_id}.webp")
                await message.delete()
        if message.reply_to_message.text \
                and message.reply_to_message.sender_chat:
            if message.reply_to_message.sender_chat.photo:
                a = await client.download_media(message.reply_to_message.sender_chat.photo.small_file_id)
                avatar = Image.open(f"{a}")
                size = (100, 100)
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                avatar = avatar.resize(size)
                output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                output.thumbnail(size, Image.ANTIALIAS)
            else:
                avatar = Image.new('RGBA', (100, 100), (255, 202, 144, 1))
                size = (100, 100)
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                avatar = avatar.resize(size)
                output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                output.thumbnail(size, Image.ANTIALIAS)
                avater_text_font = ImageFont.truetype(BytesIO(f), 40)
                avatar_text_draw = ImageDraw.Draw(output)
                avatar_text_draw.multiline_text((35, 25), list(message.reply_to_message.sender_chat.title)[0],
                                                font=avater_text_font,
                                                fill=(255, 255, 255))
            try:
                reply_msg = await client.get_messages(message.chat.id,
                                                      reply_to_message_ids=message.reply_to_message.message_id)
                count = 0
                text = ""
                for _ in message.reply_to_message.text.split():
                    if count != 9:
                        text += f" {_}"
                        count += 1
                    else:
                        count = 0
                        text += f"\n{_}"
                font_test = ImageFont.truetype(BytesIO(f), 40)
                list_size = []
                for _ in text.split("\n"):
                    ize = font_test.getsize(_)
                    list_size.append(int(str(ize).split()[0].split("(")[1].split(",")[0]))
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.sender_chat.title)
                reply_first_name_font = ImageFont.truetype(BytesIO(f), 25)
                reply_text_font = ImageFont.truetype(BytesIO(f), 35)
                if reply_msg.from_user:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.from_user.first_name)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.from_user.first_name
                elif reply_msg.sender_chat:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.sender_chat.title)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.sender_chat.title
                if reply_msg.text:
                    if len(list(reply_msg.text)) > 15:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = font_name.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                    else:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = reply_text_font.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.document:
                    msg = "Document"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.photo:
                    msg = "Photo"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.animation:
                    msg = "GIF"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.voice:
                    msg = "Voice"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.audio:
                    msg = "Audio"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.sticker:
                    msg = "Sticker"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                else:
                    msg = "Unsupported type"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                width = max(list_size) + int(str(size_name).split()[0].split("(")[1].split(",")[0]) + int(
                    ((size_rep_name + reply_tex_size) / 2))
                tab = 50 * (len(text.split("\n")) + 1)
                im = Image.new("RGBA", (width + 40, tab + 150), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                draw.line((25, 50, 25, 155), fill=(255, 255, 255), width=4)

                reply_first_name_draw = ImageDraw.Draw(im)
                reply_text_draw = ImageDraw.Draw(im)
                reply_first_name_draw.multiline_text((40, 60),
                                                     name,
                                                     font=reply_first_name_font,
                                                     fill=(10, 151, 240))
                reply_text_draw.multiline_text((40, 90),
                                               msg,
                                               font=reply_text_font,
                                               fill=(255, 255, 255))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                text_font = ImageFont.truetype(BytesIO(f), 40)
                text_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.sender_chat.title,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                text_draw.multiline_text((25, 165),
                                         text,
                                         font=text_font,
                                         fill=(255, 255, 255))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
            except:
                count = 0
                text = ""
                for _ in message.reply_to_message.text.split():
                    if count != 9:
                        text += f" {_}"
                        count += 1
                    else:
                        count = 0
                        text += f"\n{_}"
                font_test = ImageFont.truetype(BytesIO(f), 40)
                list_size = []
                for _ in text.split("\n"):
                    ize = font_test.getsize(_)
                    list_size.append(int(str(ize).split()[0].split("(")[1].split(",")[0]))
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.sender_chat.title)
                width = max(list_size) + int(str(size_name).split()[0].split("(")[1].split(",")[0])
                tab = 50 * (len(text.split("\n")) + 1)
                im = Image.new("RGBA", (width + 40, tab + 40), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                text_font = ImageFont.truetype(BytesIO(f), 40)
                text_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.sender_chat.title,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                text_draw.multiline_text((25, 55),
                                         text,
                                         font=text_font,
                                         fill=(255, 255, 255))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
            await message.reply_to_message.reply_document(f"downloads/{message.message_id}.webp")
            await message.delete()
        if not message.reply_to_message.text \
                and message.reply_to_message.sender_chat:
            if message.reply_to_message.sender_chat.photo:
                a = await client.download_media(message.reply_to_message.sender_chat.photo.small_file_id)
                avatar = Image.open(f"{a}")
                size = (100, 100)
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                avatar = avatar.resize(size)
                output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                output.thumbnail(size, Image.ANTIALIAS)
            else:
                avatar = Image.new('RGBA', (100, 100), (255, 202, 144, 1))
                size = (100, 100)
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                avatar = avatar.resize(size)
                output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
                output.putalpha(mask)
                output.thumbnail(size, Image.ANTIALIAS)
                avater_text_font = ImageFont.truetype(BytesIO(f), 40)
                avatar_text_draw = ImageDraw.Draw(output)
                avatar_text_draw.multiline_text((35, 25), list(message.reply_to_message.sender_chat.title)[0],
                                                font=avater_text_font,
                                                fill=(255, 255, 255))
            try:
                reply_msg = await client.get_messages(message.chat.id,
                                                      reply_to_message_ids=message.reply_to_message.message_id)
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.sender_chat.title)
                reply_first_name_font = ImageFont.truetype(BytesIO(f), 25)
                reply_text_font = ImageFont.truetype(BytesIO(f), 35)
                if reply_msg.from_user:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.from_user.first_name)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.from_user.first_name
                elif reply_msg.sender_chat:
                    reply_name_size = reply_first_name_font.getsize(reply_msg.sender_chat.title)
                    size_rep_name = int(str(reply_name_size).split()[0].split("(")[1].split(",")[0])
                    name = reply_msg.sender_chat.title
                if reply_msg.text:
                    if len(list(reply_msg.text)) > 15:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = font_name.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                    else:
                        msg = "".join(list(reply_msg.text)[:15])
                        reply_text_size = reply_text_font.getsize(msg)
                        reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.document:
                    msg = "Document"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.photo:
                    msg = "Photo"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.animation:
                    msg = "GIF"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.voice:
                    msg = "Voice"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.audio:
                    msg = "Audio"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                elif reply_msg.sticker:
                    msg = "Sticker"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                else:
                    msg = "Unsupported type"
                    reply_text_size = reply_text_font.getsize(msg)
                    reply_tex_size = int(str(reply_text_size).split()[0].split("(")[1].split(",")[0])
                y_n = int(str(size_name).split()[1].split(")")[0])
                width = int(str(size_name).split()[0].split("(")[1].split(",")[0]) + int(
                    (size_rep_name + reply_tex_size) + ((size_rep_name + reply_tex_size) / 2))
                im = Image.new("RGBA", (width + 40, y_n + 150), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                draw.line((25, 50, 25, 155), fill=(255, 255, 255), width=4)

                reply_first_name_draw = ImageDraw.Draw(im)
                reply_text_draw = ImageDraw.Draw(im)
                reply_first_name_draw.multiline_text((40, 60),
                                                     name,
                                                     font=reply_first_name_font,
                                                     fill=(10, 151, 240))
                reply_text_draw.multiline_text((40, 90),
                                               msg,
                                               font=reply_text_font,
                                               fill=(255, 255, 255))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.sender_chat.title,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
                await message.reply_to_message.reply_document(f"downloads/{message.message_id}.webp")
                await message.delete()
            except:
                font_name = ImageFont.truetype(BytesIO(f), 30)
                size_name = font_name.getsize(message.reply_to_message.sender_chat.title)
                x_n = int(str(size_name).split()[0].split("(")[1].split(",")[0])
                y_n = int(str(size_name).split()[1].split(")")[0])
                im = Image.new("RGBA", (x_n + 100, y_n + 100), (0, 0, 0, 0))
                x, y = im.size
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle(xy=(0, 0, x, y), radius=15, fill=(3, 29, 45))
                first_name_font = ImageFont.truetype(BytesIO(f), 30)
                first_name_draw = ImageDraw.Draw(im)
                first_name_draw.multiline_text((25, 10),
                                               message.reply_to_message.sender_chat.title,
                                               font=first_name_font,
                                               fill=(10, 151, 240))
                template_msg = Image.new("RGBA", (x + 110, y + 110), (0, 0, 0, 0))
                template_msg.paste(im, (110, 0))
                template_msg.paste(output, (0, 0))
                template_msg.save(f"downloads/{message.message_id}.webp")
                await message.reply_to_message.reply_document(f"downloads/{message.message_id}.webp")
                await message.delete()
    else:
        await message.edit("Reply on user message")


modules_help.update({'mquotes': '''mquote - Reply on user message''',
                     'mquotes module': 'MQuotes: mquote\n'})
