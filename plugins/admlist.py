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

import json
from html import escape as t
from time import perf_counter

from pyrogram import Client, filters
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.raw.functions.messages.get_all_chats import GetAllChats
from pyrogram.types import Message

from .utils.utils import modules_help, prefix


@Client.on_message(filters.command("admlist", prefix) & filters.me)
async def ownlist(client: Client, message: Message):
    tstart = perf_counter()
    await message.edit("<code>Retrieving information... (it'll take some time)</code>")
    chatlist = []
    try:
        _ = await client.send(GetAllChats(except_ids=[]))
        chats = json.loads(str(_))
        for chat in chats["chats"]:
            if chat.get("migrated_to") is None and (
                chat.get("creator") is True or chat.get("admin_rights") is not None
            ):
                role = "creator" if chat.get("creator") is True else "administrator"
                chatlist.append(
                    {
                        "chat_name": str(chat["title"]),
                        "chat_id": chat["id"],
                        "role": role,
                        "username": chat.get("username"),
                        "link": "https://t.me/c/{}/1".format(chat["id"]),
                    }
                )

        adminned_chats = "<b>Adminned chats:</b>\n"
        owned_chats = "<b>Owned chats:</b>\n"
        owned_chats_with_username = "<b>Owned chats with username:</b>\n"

        c_adminned_chats = 0
        c_owned_chats = 0
        c_owned_chats_with_username = 0

        for chat in chatlist:
            if chat["role"] == "creator" and chat["username"] is not None:
                c_owned_chats_with_username += 1
                owned_chats_with_username += f'{c_owned_chats_with_username}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a> - @{chat["username"]}\n'
            elif chat["role"] == "creator":
                c_owned_chats += 1
                owned_chats += f'{c_owned_chats}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a>\n'
            elif chat["role"] == "administrator":
                c_adminned_chats += 1
                adminned_chats += f'{c_adminned_chats}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a>\n'
        stats = f"<b><u>Total:</u></b> {len(chatlist)}\n<b><u>Adminned chats:</u></b> {c_adminned_chats}\n<b><u>Owned chats:</u></b> {c_owned_chats}\n<b><u>Owned chats with username:</u></b> {c_owned_chats_with_username}"
        tstop = perf_counter()
        await message.edit(
            adminned_chats
            + "\n"
            + owned_chats
            + "\n"
            + owned_chats_with_username
            + "\n"
            + stats
            + "\n\n"
            + f"Done at {int(tstop - tstart)} seconds.",
            disable_web_page_preview=True,
        )
    except FloodWait as e:
        await message.edit(
            "<b>Error occured.</b>\n<code>FloodWait. Try again in {} seconds</code>".format(
                e.x
            )
        )


modules_help.append({"admlist": [{"admlist": "Get adminned and owned chats"}]})
