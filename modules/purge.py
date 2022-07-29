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

import asyncio
from requests import get
from datetime import datetime
from inspect import getfullargspec
from pyrogram.errors import RPCError
from pyrogram import filters, enums
from pyrogram.types import Message


@Client.on_message(filters.command("purge", prefix) & filters.me)
async def purge_message(client: Client, message): Message:
    try:
        if message.reply_to_message:
            start = datetime.now()
            y = await client.get_messages(
                                message.chat.id,
                                range(message.reply_to_message.id, message.id),
                                replies=0
                        )
            msg_id = []
            msg_id.clear()
            for msg in y:
                 msg_id.append(msg.id)
            await app.delete_messages(
                                message.chat.id,
                                msg_id
                        )
            sec = (datetime.now() - start).seconds
            await message.edit(f"Deleted `{len(msg_id)}` messages in `{sec}` seconds.")
            await asyncio.sleep(5)
            await message.delete()
        else:
            await message.edit("Reply to message you want to delete from.")
    except RPCError:
        await message.edit("I can't do that.")


@Client.on_message(filters.command("del", prefix) & filters.me)
async def delete_replied(client: Client, message: Message):
    msg_ids = [message.id]
    if message.reply_to_message:
        msg_ids.append(message.reply_to_message.id)
    await app.delete_messages(message.chat.id, msg_ids)


@Client.on_message(filters.command("purgeme", prefix) & filters.me)
async def purge_me(client: Client, message: Message):
    if len(message.command) != 2:
        return
    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await message.edit("Give me a number not a strings.")
    n = int(n)
    if n < 1:
        return await message.edit("Give me a number total message you want to delete.")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user="me",
            limit=n,
        )
    ]
    if not message_ids:
        return await message.edit("Pesan tidak di temukan")
    to_delete = [message_ids[i : i + 99] for i in range(0, len(message_ids), 99)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
    ms_g = await client.send_message(
        message.chat.id,
        f"Successfully delete <code>{n}</code> message.",
    )
    await asyncio.sleep(5)
    await ms_g.delete()


@Client.on_message(filters.command("purgeall", prefix) & filters.me)
async def purge_all(client: Client, message: Message):
    y = message.reply_to_message
    if not y:
        await message.edit("reply to a user message or to your message to start purgeall.")
        return
    else:
        try:
            turok = y.from_user.id
            bisa = await client.get_users(turok)
            await message.edit("Starting delete messages.")
            await client.delete_user_history(message.chat.id, bisa.id)
        except RPCError:
            await message.edit("Sorry you're not admin.")


modules_help["purge"] = {
    "purge [reply]": "Purge (delete all messages) chat from replied message to last",
    "del [reply]": "Delete replied message",
    "purgeme [total_msg]": "Delete your own messages with specify total messages",
    "purgeall [reply]": "[Be carefull use this] Delete all your message or your replied message",
}
