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

import time

from pyrogram import Client, filters
from pyrogram.types import Message
from platform import python_version
from pyrogram import __version__ as k
from utils.misc import modules_help, prefix
from utils import config


ALIVE_TEXT = """
<b>Hey I am Alive!</b>

XUB is online!

<b>Python:</b> <code>{}</code>
<b>Pyrogram:</b> <code>{}</code>
<b>XUB Version:</b> <code>master@0.0.1</code>
<b>My Master:</b> {}
"""


@Client.on_message(filters.command(["ping"], prefix) & filters.me)
async def ping(_, message: Message):
    start = time.time()
    reply = await message.edit("Pinging...")
    delta_ping = time.time() - start
    await reply.edit(f"**Pong!**\n`{delta_ping * 1000:.3f} ms`")

@Client.on_message(filters.command(["alive"], prefix) & filters.me)
async def alive(_, m: Message):
    if config.alive.endswith(".jpg"):
        return await _.send_photo(
            m.chat.id,
            photo=config.alive,
            caption=ALIVE_TEXT
                .format(python_version(), k, _.me.mention)
        )
    elif config.alive.endswith(".mp4"):
        return await _.send_video(
            m.chat.id,
            video=config.alive,
            caption=ALIVE_TEXT
                .format(python_version(), k, _.me.mention)
        )
    else:
        return m.edit(
            ALIVE_TEXT
                .format(python_version(), k, _.me.mention)
        )


@Client.on_message(filters.command(["repo"], prefix) & filters.me)
async def repos(_, m: Message):
    await m.edit(
        "I am using XUB"
        "XUB version: <code>master@0.0.1</code>"
        "Python version: <code>{}</code>"
        "Pyrogram version: <code>{}</code>"
            .format(python_version(), k)
    )


modules_help["ping"] = {
    "ping": "Check ping to Telegram servers",
    "alive": "Get alive XUB",
}
