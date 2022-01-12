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


@Client.on_message(filters.command("del", prefix) & filters.me)
async def del_msg(client: Client, message: Message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        await message.delete()
        await client.delete_messages(message.chat.id, message_id)


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


modules_help.append(
    {
        "purge": [
            {
                "purge [reply]*": "Reply to a message after which you want to delete messages"
            },
            {"del [reply]*": "Reply to the message you want to delete"},
        ]
    }
)
