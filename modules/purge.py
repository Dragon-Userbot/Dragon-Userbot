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

from pyrogram import Client, filters
from pyrogram.types import Message

import asyncio

from utils.misc import modules_help, prefix
from utils.scripts import with_reply


@Client.on_message(filters.command("del", prefix) & filters.me)
async def del_msg(_, message: Message):
    await message.delete()
    await message.reply_to_message.delete()


@Client.on_message(filters.command("purge", prefix) & filters.me)
async def purge(client: Client, message: Message):
    messages_to_purge = []
    if message.reply_to_message:
        async for msg in client.iter_history(
            chat_id=message.chat.id,
            offset_id=message.reply_to_message.message_id,
            reverse=True,
        ):
            messages_to_purge.append(msg.message_id)
    not_deleted_messages = []
    for msgs in [
        messages_to_purge[i : i + 100] for i in range(0, len(messages_to_purge), 100)
    ]:
        res = await client.delete_messages(message.chat.id, msgs)
        await asyncio.sleep(1)

modules_help["purge"] = {
    "purge [reply]": "Purge (delete all messages) chat from replied message to last",
    "del [reply]": "Delete replied message",
}
