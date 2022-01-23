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

from utils.misc import modules_help, prefix
from utils.scripts import format_exc


@Client.on_message(filters.command("admcount", prefix) & filters.me)
async def admcount(client: Client, message: Message):
    await message.edit("<b>Retrieving information... (it'll take some time)</b>")

    start = perf_counter()
    try:
        response = await client.send(GetAllChats(except_ids=[]))
        chats = response["chats"]

        adminned_chats = 0
        owned_chats = 0
        owned_usernamed_chats = 0

        for chat in chats:
            if getattr(chat, "migrated_to", None):
                continue
            if chat.creator and getattr(chat, "username", None):
                owned_usernamed_chats += 1
            elif chat.creator:
                owned_chats += 1
            elif getattr(chat, "admin_rights", None):
                adminned_chats += 1
    except Exception as e:
        await message.edit(format_exc(e))
        return

    stop = perf_counter()

    await message.edit(
        f"<b><u>Total:</u></b> {adminned_chats + owned_chats + owned_usernamed_chats}"
        f"\n<b><u>Adminned chats:</u></b> {adminned_chats}\n"
        f"<b><u>Owned chats:</u></b> {owned_chats}\n"
        f"<b><u>Owned chats with username:</u></b> {owned_usernamed_chats}\n\n"
        f"Done at {round(stop - start, 3)} seconds.\n\n"
        f"<b>Get full list: </b><code>{prefix}admlist</code>"
    )


@Client.on_message(filters.command("admlist", prefix) & filters.me)
async def admlist(client: Client, message: Message):
    await message.edit("<b>Retrieving information... (it'll take some time)</b>")

    start = perf_counter()
    try:
        response = await client.send(GetAllChats(except_ids=[]))
        chats = response["chats"]

        adminned_chats = []
        owned_chats = []
        owned_usernamed_chats = []

        for chat in chats:
            if getattr(chat, "migrated_to", None) is not None:
                continue
            if chat.creator and getattr(chat, "username", None):
                owned_usernamed_chats.append(chat)
            elif chat.creator:
                owned_chats.append(chat)
            elif getattr(chat, "admin_rights", None):
                adminned_chats.append(chat)

        text = "<b>Adminned chats:</b>\n"
        for index, chat in enumerate(adminned_chats):
            text += (
                f"{index + 1}. <a href=https://t.me/c/{chat.id}/1>{chat.title}</a>\n"
            )

        text += "\n<b>Owned chats:</b>\n"
        for index, chat in enumerate(owned_chats):
            text += (
                f"{index + 1}. <a href=https://t.me/c/{chat.id}/1>{chat.title}</a>\n"
            )

        text += "\n<b>Owned chats with username:</b>\n"
        for index, chat in enumerate(owned_usernamed_chats):
            text += (
                f"{index + 1}. <a href=https://t.me/{chat.username}>{chat.title}</a>\n"
            )

        stop = perf_counter()
        total_count = (
            len(adminned_chats) + len(owned_chats) + len(owned_usernamed_chats)
        )
        await message.edit(
            text + "\n"
            f"<b><u>Total:</u></b> {total_count}"
            f"\n<b><u>Adminned chats:</u></b> {len(adminned_chats)}\n"
            f"<b><u>Owned chats:</u></b> {len(owned_chats)}\n"
            f"<b><u>Owned chats with username:</u></b> {len(owned_usernamed_chats)}\n\n"
            f"Done at {round(stop - start, 3)} seconds."
        )
    except Exception as e:
        await message.edit(format_exc(e))
        return


modules_help["admlist"] = {
    "admcount": "Get count of adminned and owned chats",
    "admlist": "Get list of adminned and owned chats",
}
