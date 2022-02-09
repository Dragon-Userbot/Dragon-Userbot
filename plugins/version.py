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

from .utils import utils
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command(["version", "ver"], prefix) & filters.me)
async def version(client: Client, message: Message):
    changelog = ""
    async for m in client.search_messages(
        "dRaGoN_uB_cHaNgElOg", query=utils.version.split(".")[0]
    ):
        if utils.version in m.text:
            changelog = m.message_id
    await message.delete()
    await message.reply(
        f"<b>Version</b> <code>{utils.version}</code>.\n"
        f"<b>Changelog</b> <i><a href=https://t.me/dRaGoN_uB_cHaNgElOg/{changelog}>in channel</a></i>.\n"
        f"<b>Changelog are written by<a href=tg://user?id=318865588>\u2060</a></b> <a href=tg://user?id=293490416>♿️</a><i><a href=https://t.me/LKRinternationalrunetcomphinc>asphuy</a><a href=https://t.me/artemjj2>♿️</a></i>."
    )


modules_help.append({"version": [{"version": "Userbot version and changelog"}]})
