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

# rewrote the module from @ Fl1yd
import asyncio
import os

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from .utils.db import db
from .utils.utils import modules_help, prefix


def get_pic(city):
    file_name = f"{city}.png"
    with open(file_name, "wb") as pic:
        response = requests.get(f"http://wttr.in/{city}_2&lang=en.png", stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            pic.write(block)
        return file_name


@Client.on_message(filters.command("weather", prefix) & filters.me)
async def weather(client: Client, message: Message):
    try:
        city = message.command[1]
        await message.edit("```Processing the request...```")
        r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
        await message.edit(f"```City: {r.text}```")
        await client.send_document(
            chat_id=message.chat.id,
            document=get_pic(city),
            reply_to_message_id=message.message_id,
        )
        os.remove(f"{city}.png")
    except:
        await message.edit("<code>Error occured</code>")
        await asyncio.sleep(5)
        await message.delete()


@Client.on_message(filters.command("set_weather_city", prefix) & filters.me)
async def set_weather_city(client: Client, message: Message):
    try:
        db.set("core.weather", "city", message.command[1])
        await message.edit("<code>City set-upped.</code>")
    except:
        await message.edit("<code>Error occured.</code>")


@Client.on_message(filters.command("w", prefix) & filters.me)
async def w(client: Client, message: Message):
    try:
        city = db.get("core.weather", "city", "Moscow")
        await message.edit("```Processing the request...```")
        r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
        await message.edit(f"```City: {r.text}```")
        await client.send_document(
            chat_id=message.chat.id,
            document=get_pic(city),
            reply_to_message_id=message.message_id,
        )
        os.remove(f"{city}.png")
    except:
        await message.edit("<code>Error occured</code>")
        await asyncio.sleep(5)
        await message.delete()


modules_help.append(
    {
        "weather": [
            {"weather [city]*": "Get the weather in the selected city"},
            {"set_weather_city [city]*": "Set city for w command"},
            {"w": "Quick access to set city (Moscow if nothing was set)"},
        ]
    }
)
