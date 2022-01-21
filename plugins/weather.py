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
from io import BytesIO

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.db import db
from utils.misc import modules_help, prefix
from utils.scripts import format_exc


@Client.on_message(filters.command(["weather", "w"], prefix) & filters.me)
async def weather(client: Client, message: Message):
    if len(message.command) == 1:
        city = db.get("core.weather", "city", "Moscow")
    else:
        city = message.command[1]

    await message.edit(f"<b>Processing city {city}...</b>")

    try:
        text_resp = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
        text_resp.raise_for_status()
        caption = f"```City: {text_resp.text}```"

        pic_resp = requests.get(f"http://wttr.in/{city}_2&lang=en.png")
        pic_resp.raise_for_status()
        pic = BytesIO(pic_resp.content)
        pic.name = f"{city}.png"

        await client.send_document(
            chat_id=message.chat.id, document=pic, caption=caption
        )
        await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command(["set_weather_city", "swcity"], prefix) & filters.me)
async def set_weather_city(_, message: Message):
    if len(message.command) == 1:
        return await message.edit("<b>City name isn't provided</b>")

    db.set("core.weather", "city", message.command[1])
    await message.edit(f"<b>City {message.command[1]} set!</b>")


modules_help["weather"] = {
    "weather [city]*": "Get weather for selected city or chosen in set_weather_city",
    "set_weather_city [city]*": f"Set city for {prefix}weather command, Moscow by default",
}
