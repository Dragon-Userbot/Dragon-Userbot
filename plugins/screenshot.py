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
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(
    filters.command(["scr", "screenshot"], prefix) & filters.private & filters.me
)
async def screenshot(client: Client, message: Message):
    amount = int(message.command[1]) if len(message.command) > 1 else 1
    await message.delete()
    for _ in range(amount):
        await client.send(
            functions.messages.SendScreenshotNotification(
                peer=await client.resolve_peer(message.chat.id),
                reply_to_msg_id=0,
                random_id=client.rnd_id(),
            )
        )
        await asyncio.sleep(0.1)


modules_help["screenshot"] = {
    "scr [amount]": 'Send "You took a screenshot" message. Works only in PM'
}
