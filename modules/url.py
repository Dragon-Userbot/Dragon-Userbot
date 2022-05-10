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
import os

from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from utils.misc import modules_help, prefix
from utils.scripts import format_exc


@Client.on_message(filters.command("short", prefix) & filters.me)
async def short(_, message: Message):
    if len(message.command) > 1:
        link = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        link = message.reply_to_message.text
    else:
        await message.edit(f"<b>Usage: </b><code>{prefix}short [url to short]</code>")
        return

    shortened = requests.get("https://clck.ru/--", data={"url": link}).text

    await message.edit(shortened.replace("https://", ""), disable_web_page_preview=True)


@Client.on_message(filters.command("urldl", prefix) & filters.me)
async def urldl(client: Client, message: Message):
    if len(message.command) > 1:
        link = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        link = message.reply_to_message.text
    else:
        await message.edit(
            f"<b>Usage: </b><code>{prefix}urldl [url to download]</code>"
        )
        return

    await message.edit("<b>Downloading...</b>")
    file_name = "downloads/" + link.split("/")[-1]

    try:
        resp = requests.get(link)
        resp.raise_for_status()

        with open(file_name, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        await message.edit("<b>Uploading...</b>")
        await client.send_document(message.chat.id, file_name)
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))
    finally:
        os.remove(file_name)


@Client.on_message(filters.command("upload", prefix) & filters.me)
async def upload_cmd(_, message: Message):
    max_size = 512 * 1024 * 1024
    max_size_mb = 512

    min_file_age = 31
    max_file_age = 180

    await message.edit("<b>Downloading...</b>")

    try:
        file_name = await message.download()
    except ValueError:
        try:
            file_name = await message.reply_to_message.download()
        except ValueError:
            await message.edit("<b>File to upload not found</b>")
            return

    if os.path.getsize(file_name) > max_size:
        await message.edit(f"<b>Files longer than {max_size_mb}MB isn't supported</b>")
        os.remove(file_name)
        return

    await message.edit("<b>Uploading...</b>")
    with open(file_name, "rb") as f:
        response = requests.post(
            "https://x0.at",
            files={"file": f},
        )

    if response.ok:
        file_size_mb = os.path.getsize(file_name) / 1024 / 1024
        file_age = int(
            min_file_age
            + (max_file_age - min_file_age) * ((1 - (file_size_mb / max_size_mb)) ** 2)
        )
        url = response.text.replace("https://", "")
        await message.edit(
            f"<b>Your URL: {url}\nYour file will live {file_age} days</b>",
            disable_web_page_preview=True,
        )
    else:
        await message.edit(f"<b>API returned an error!\n{response.text}</b>")

    os.remove(file_name)


@Client.on_message(filters.command("webshot", prefix) & filters.me)
async def webshot(client: Client, message: Message):
    try:
        user_link = message.command[1]
        await message.delete()
        full_link = f"https://webshot.deam.io/{user_link}/?delay=2000"
        await client.send_document(message.chat.id, full_link, caption=f"{user_link}")
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["url"] = {
    "short [url]*": "short url",
    "urldl [url]*": "download url content",
    "upload [file|reply]*": "upload file to internet",
    "webshot [link]*": "Screenshot of web page",
}
