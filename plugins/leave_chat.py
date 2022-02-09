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

from pyrogram import Client, filters
from pyrogram.types import Message

from .utils.utils import modules_help, prefix


@Client.on_message(filters.command(["leave_chat", "lc"], prefix) & filters.me)
async def leave_chat(client: Client, message: Message):
    if message.chat.type in ["group", "supergroup"]:
        await message.edit("<code>Goodbye...</code>")
        await asyncio.sleep(3)
        await client.leave_chat(chat_id=message.chat.id)
    else:
        await message.edit("This is not a group/suppergroup")


modules_help.append({"leave_chat": [{"leave_chat": "Quit chat"}]})
