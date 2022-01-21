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

import asyncio

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


def getpic(query):
    return eval(requests.get(f"https://nekos.life/api/v2/img/{query}").text)["url"]


@Client.on_message(filters.command("neko", prefix) & filters.me)
async def neko(client: Client, message: Message):
    await message.edit("<code>Wait...</code>")
    try:
        query = message.command[1]
        await message.edit(f"{getpic(query)}", disable_web_page_preview=False)
    except:
        await message.edit("<code>Error\nYou entered the wrong type for it</code>")


@Client.on_message(filters.command("neko_types", prefix) & filters.me)
async def neko_types_func(client: Client, message: Message):
    neko_t = """femdom tickle classic ngif erofeet meow erok poke les hololewd lewdk keta feetg nsfw_neko_gif eroyuri kiss 8ball kuni tits pussy_jpg cum_jpg pussy lewdkemo lizard slap lewd cum cuddle spank smallboobs goose Random_hentai_gif avatar fox_girl nsfw_avatar hug gecg boobs pat feet smug kemonomimi solog holo wallpaper bj woof yuri trap anal baka blowjob holoero feed neko gasm hentai futanari ero solo waifu pwankg eron erokemo"""
    neko_types = "".join(f"<code>{ntype}</code>  " for ntype in neko_t.split())
    await message.edit(neko_types)


@Client.on_message(filters.command("nekospam", prefix) & filters.me)
async def neko_spam(client: Client, message: Message):
    await message.delete()
    query = " ".join(message.command[2:])
    quantity = int(message.command[1])
    for _ in range(quantity):
        await client.send_message(
            message.chat.id, getpic(query), disable_web_page_preview=False
        )
        await asyncio.sleep(0.2)


modules_help.append(
    {
        "neko": [
            {"neko [type]* [amount of spam]": "For get neko media"},
            {"neko_types": "Available neko types"},
        ]
    }
)
