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
from platform import python_version as yy
from pyrogram import __version__ as k
from utils.misc import modules_help, prefix
from utils import config


ALIVE_TEXT = """<b>Hey I am Alive!</b>

XUB is online!

<b>Uptime:</b> <code>{}</code>
<b>Python:</b> <code>{}</code>
<b>Pyrogram:</b> <code>{}</code>
<b>XUB Version:</b> <code>master@0.0.1</code>
"""

StartTime = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


@Client.on_message(filters.command(["ping"], prefix) & filters.me)
async def ping(_, message: Message):
    start_time = time.time()
    uptime = get_readable_time((time.time() - StartTime))
    reply = await message.edit("Pinging...")
    end_time = time.time()
    delta_ping = time.time() - start_time
    await reply.edit(
        f"🏓 <b>Pong!</b> <code>{delta_ping * 1000:.3f} ms</code>"
        f"\n⏱️ <b>Uptime -</b> <code>{uptime}</code>"
    )

@Client.on_message(filters.command(["alive"], prefix) & filters.me)
async def alive(_, m: Message):
    start_time = time.time()
    uptime = get_readable_time((time.time() - StartTime))
    end_time = time.time()
    if config.alive.endswith(".jpg"):
        return await _.send_photo(
            m.chat.id,
            photo=config.alive,
            caption=ALIVE_TEXT
                .format(uptime, yy(), k, _.me.mention),
        )
    elif config.alive.endswith(".mp4"):
        return await _.send_video(
            m.chat.id,
            video=config.alive,
            caption=ALIVE_TEXT
                .format(uptime, yy(), k, _.me.mention),
        )
    else:
        return await m.edit(
            ALIVE_TEXT
                .format(uptime, yy(), k, _.me.mention),
        )


@Client.on_message(filters.command(["repo"], prefix) & filters.me)
async def repos(_, m: Message):
    await m.edit(
        "I am using XUB"
        "\n\nXUB version: <code>master@0.0.1</code>"
        "\nPython version: <code>{}</code>"
        "\nPyrogram version: <code>{}</code>"
        "\nRepository link: <a href='https://github.com/kennedy-ex/XUB'>XUB</a>"
            .format(piton, k),
        disable_web_page_preview=True
    )


modules_help["ping"] = {
    "ping": "Check ping to Telegram servers",
    "alive": "Get alive XUB",
    "repo": "Show link repository of XUB",
}
