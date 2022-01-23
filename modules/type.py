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
import time

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("type", prefix) & filters.me)
async def type(client: Client, message: Message):
    orig_text = " ".join(message.command[1:])
    text = orig_text
    tbp = ""
    typing_symbol = "▒"

    while text: # while the text string is not empty
        try:
            await message.edit(tbp + typing_symbol)
            await asyncio.sleep(0.1)

            tbp += text[0]
            text = text[1:]

            await message.edit(tbp)
            await asyncio.sleep(0.1)

        except FloodWait as e:
            time.sleep(e.x)


modules_help.append(
    {
        "type": [
            {
                "type [text]*": "Typing emulation\nDon't use for a lot of characters. Your account may be banned!"
            }
        ]
    }
)
