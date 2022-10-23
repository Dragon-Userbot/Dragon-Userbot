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

from utils.misc import modules_help, prefix
from utils.scripts import with_reply


@Client.on_message(filters.command("del", prefix) & filters.me)
async def del_msg(_, message: Message):
    await message.delete()
    await message.reply_to_message.delete()


@Client.on_message(filters.command("purge", prefix) & filters.me)
@with_reply
async def purge(client: Client, message: Message):
    chunk = []
    async for msg in client.get_chat_history(
        chat_id=message.chat.id,
        limit=message.id - message.reply_to_message.id + 1,
    ):
        if msg.id < message.reply_to_message.id:
            break
        chunk.append(msg.id)
        if len(chunk) >= 100:
            await client.delete_messages(message.chat.id, chunk)
            chunk.clear()
            await asyncio.sleep(1)

    if len(chunk) > 0:
        await client.delete_messages(message.chat.id, chunk)


modules_help["purge"] = {
    "purge [reply]": "Purge (delete all messages) chat from replied message to last",
    "del [reply]": "Delete replied message",
}
