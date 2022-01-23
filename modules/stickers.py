#  Dragon-Userbot - telegram userbot
#  Copyright (C) 2020-present Dragon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import os

from pyrogram import Client, filters, types
from PIL import Image
import asyncio

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("kang", prefix) & filters.me)
async def kang(client: Client, message: types.Message):
    await message.edit("<b>Please wait...</b>")
    try:
        args = message.text.split(" ")
        if len(args) > 1:
            args.pop(0)
            pack = args[0]
            try:
                emoji = args[1]
            except:
                emoji = "🤔"
        else:
            await message.edit(
                "<b>No arguments provided</b>\nUsage:"
                + f"<code>{prefix}kang [pack*] [emoji]</code>"
            )
            return
    except:
        await message.edit("<b>No reply found</b>")
        return
    if message.reply_to_message:
        s = message.reply_to_message
    else:
        await message.edit("<b>No reply found</b>")
        return
    if not (s.sticker or s.photo):
        await message.edit("<b>Photo / sticker not found</b>")
    to_del = []
    to_del.append((await client.send_message("@stickers", "/cancel")))
    bot_msg = (await client.get_history("@stickers", limit=1))[0]
    while bot_msg.from_user.is_self:
        await asyncio.sleep(1)
        bot_msg = (await client.get_history("@stickers", limit=1))[0]
    to_del.append(bot_msg)
    to_del.append((await client.send_message("@stickers", "/addsticker")))
    bot_msg = (await client.get_history("@stickers", limit=1))[0]
    while bot_msg.from_user.is_self:
        await asyncio.sleep(1)
        bot_msg = (await client.get_history("@stickers", limit=1))[0]
    to_del.append(bot_msg)
    to_del.append((await client.send_message("@stickers", pack)))
    bot_msg = (await client.get_history("@stickers", limit=1))[0]
    while bot_msg.from_user.is_self:
        await asyncio.sleep(1)
        bot_msg = (await client.get_history("@stickers", limit=1))[0]
    to_del.append(bot_msg)
    if ".TGS" in bot_msg.text:
        await message.edit("<b>Animated packs aren't supported.</b>")
        return
    if bot_msg.text.split()[0] == "Alright!":
        path = await s.download()
        if path:
            p2 = "stik" + datetime.datetime.now().isoformat() + ".png"
            resize_image(path, (512, 512), p2)
            to_del.append((await client.send_document("@stickers", p2)))
            bot_msg = (await client.get_history("@stickers", limit=1))[0]
            while bot_msg.from_user.is_self:
                await asyncio.sleep(1)
                bot_msg = (await client.get_history("@stickers", limit=1))[0]
            to_del.append(bot_msg)
            os.remove(path)
            os.remove(p2)
            bot_msg = (await client.get_history("@stickers", limit=1))[0]
            while bot_msg.from_user.is_self:
                await asyncio.sleep(1)
                bot_msg = (await client.get_history("@stickers", limit=1))[0]
            to_del.append(bot_msg)
            to_del.append((await client.send_message("@stickers", emoji)))
            bot_msg = (await client.get_history("@stickers", limit=1))[0]
            while bot_msg.from_user.is_self:
                await asyncio.sleep(1)
                bot_msg = (await client.get_history("@stickers", limit=1))[0]
            to_del.append(bot_msg)
            if "added your sticker" in bot_msg.text:
                to_del.append((await client.send_message("@stickers", "/done")))
                bot_msg = (await client.get_history("@stickers", limit=1))[0]
                while bot_msg.from_user.is_self:
                    await asyncio.sleep(1)
                    bot_msg = (await client.get_history("@stickers", limit=1))[0]
                to_del.append(bot_msg)
                await message.edit(
                    f'<b>Sticker added to <a href="https://t.me/addstickers/{pack}">pack</a></b>'
                )
                await client.delete_messages(
                    "@stickers", [msg.message_id for msg in to_del]
                )
            else:
                await message.edit("<b>Something went wrong</b>")
        else:
            await message.edit("<b>Unknown error occured</b>")
            await client.delete_messages(
                "@stickers", [msg.message_id for msg in to_del]
            )
    else:
        await client.delete_messages("@stickers", [msg.message_id for msg in to_del])
        await message.edit(
            "<b>Stickerpack doesn't exitst. Create it using @Stickers bot (via /newpack command)</b>"
        )


def resize_image(img, size, dest):
    # Wrapper for asyncio purposes
    try:
        im = Image.open(img)
        # We used to use thumbnail(size) here, but it returns with a *max* dimension of 512,512
        # rather than making one side exactly 512 so we have to calculate dimensions manually :(
        if im.width == im.height:
            size = (512, 512)
        elif im.width < im.height:
            size = (int(512 * im.width / im.height), 512)
        else:
            size = (512, int(512 * im.height / im.width))
        im.resize(size).save(dest, "PNG")
    finally:
        im.close()
        del im
