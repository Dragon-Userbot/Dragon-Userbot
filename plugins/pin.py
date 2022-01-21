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

from utils.scripts import with_reply, format_exc
from utils.misc import modules_help, prefix


@Client.on_message(filters.command("pin", prefix) & filters.me)
@with_reply
async def pin(_, message: Message):
    try:
        await message.reply_to_message.pin()
        await message.edit("<b>Pinned!</b>")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("unpin", prefix) & filters.me)
@with_reply
async def unpin(_, message: Message):
    try:
        await message.reply_to_message.unpin()
        await message.edit("<b>Unpinned!</b>")
    except Exception as e:
        await message.edit(format_exc(e))


modules_help.append(
    {
        "pin": [
            {"pin": "Pin replied message"},
            {"unpin": "Unpin replied message"},
        ]
    }
)
