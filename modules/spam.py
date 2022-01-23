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


@Client.on_message(filters.command("statspam", prefix) & filters.me)
async def statspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for _ in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.1)
        await msg.delete()
        await asyncio.sleep(0.1)


@Client.on_message(filters.command("spam", prefix) & filters.me)
async def spam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.15)
        return

    for _ in range(quantity):
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.15)


@Client.on_message(filters.command("fastspam", prefix) & filters.me)
async def fastspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.02)
        return

    for _ in range(quantity):
        await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.02)


@Client.on_message(filters.command("slowspam", prefix) & filters.me)
async def slowspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    await message.delete()

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.9)
        return

    for _ in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.9)


modules_help.append(
    {
        "spam": [
            {"spam [amount of spam]* [spam text]*": "Start spam"},
            {"statspam [amount of spam]* [spam text]*": "Send and delete"},
            {"fastspam [amount of spam]* [spam text]*": "Start fast spam"},
            {"slowspam [amount of spam]* [spam text]*": "Start slow spam"},
        ]
    }
)
