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

from .utils.db import db
from .utils.scripts import restart
from .utils.utils import modules_help, prefix


@Client.on_message(
    filters.command(["sp", "setprefix", "setprefix_dragon"], prefix) & filters.me
)
async def pref(client: Client, message: Message):
    if len(message.command) > 1:
        prefix = message.command[1]
        print(message.command)
        db.set("core.main", "prefix", prefix)
        await message.edit(f"<b>Prefix [ <code>{prefix}</code> ] is set!</b>")
        await restart()
    else:
        await message.edit("<b>The prefix must not be empty!</b>")


modules_help.append(
    {
        "prefix": [
            {"setprefix [prefix]*": "Set custom prefix"},
            {"setprefix_dragon [prefix]*": "Set custom prefix"},
        ]
    }
)
