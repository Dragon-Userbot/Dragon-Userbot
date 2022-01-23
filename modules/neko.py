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
from utils.scripts import format_exc


def get_neko_media(query):
    return requests.get(f"https://nekos.life/api/v2/img/{query}").json()["url"]


@Client.on_message(filters.command("neko", prefix) & filters.me)
async def neko(_, message: Message):
    if len(message.command) == 1:
        await message.edit(
            "<b>Neko type isn't provided\n"
            f"You can get available neko types with <code>{prefix}neko_types</code></b>"
        )

    query = message.command[1]
    await message.edit("<b>Loading...</b>")
    try:
        await message.edit(f"{get_neko_media(query)}", disable_web_page_preview=False)
    except Exception as e:
        await message.edit(format_exc(e, hint="maybe you entered wrong type"))


@Client.on_message(filters.command(["nekotypes", "neko_types"], prefix) & filters.me)
async def neko_types_func(_, message: Message):
    neko_types = """femdom tickle classic ngif erofeet meow erok poke les hololewd lewdk keta feetg nsfw_neko_gif eroyuri kiss 8ball kuni tits pussy_jpg cum_jpg pussy lewdkemo lizard slap lewd cum cuddle spank smallboobs goose Random_hentai_gif avatar fox_girl nsfw_avatar hug gecg boobs pat feet smug kemonomimi solog holo wallpaper bj woof yuri trap anal baka blowjob holoero feed neko gasm hentai futanari ero solo waifu pwankg eron erokemo"""
    await message.edit(" ".join(f"<code>{n}</code>" for n in neko_types.split()))


@Client.on_message(filters.command(["nekospam", "neko_spam"], prefix) & filters.me)
async def neko_spam(client: Client, message: Message):
    query = message.command[1]
    amount = int(message.command[2])

    await message.delete()

    for _ in range(amount):
        if message.reply_to_message:
            await message.reply_to_message.reply(get_neko_media(query))
        else:
            await client.send_message(message.chat.id, get_neko_media(query))
        await asyncio.sleep(0.1)


modules_help["neko"] = {
    "neko [type]*": "Get neko media",
    "neko_types": "Available neko types",
    "neko_spam [type]* [amount]*": "Start spam with neko media",
}
