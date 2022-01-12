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
from pyrogram.handlers import MessageHandler
from pyrogram.raw import functions
from pyrogram.types import Message

from .utils.db import db
from .utils.utils import modules_help, prefix


async def anti_pm_handler(client: Client, message: Message):
    status = db.get("core.antipm", "status", False)
    if (
        status
        and message.chat.type in ["private"]
        and (
            not message.from_user.is_contact
            and not message.from_user.is_bot
            and not message.from_user.is_self
        )
    ):
        await client.read_history(message.chat.id)
        user_info = await client.resolve_peer(message.chat.id)
        await message.delete()
        if db.get("core.antipm", "spamrep", False):
            await client.send(functions.messages.ReportSpam(peer=(user_info)))
        await client.send(
            functions.messages.DeleteHistory(peer=(user_info), max_id=0, revoke=True)
        )


@Client.on_message(filters.command(["anti_pm"], prefix) & filters.me)
async def anti_pm(client: Client, message: Message):
    status = db.get("core.antipm", "status", False)
    if status:
        await message.edit("Anti-pm enabled")
        my_handler = MessageHandler(anti_pm_handler, filters.private)
        client.add_handler(my_handler)
    else:
        db.set("core.antipm", "status", True)
        my_handler = MessageHandler(anti_pm_handler, filters.private)
        client.add_handler(my_handler)
        await message.edit("Anti-pm enabled")


@Client.on_message(filters.command(["disable_anti_pm"], prefix) & filters.me)
async def disable_anti_pm(client: Client, message: Message):
    db.set("core.antipm", "status", False)
    await message.edit("Anti-pm disabled")


@Client.on_message(filters.command(["esr"], prefix) & filters.me)
async def esr(client: Client, message: Message):
    db.set("core.antipm", "spamrep", True)
    await message.edit("Spam-reporting enabled")


@Client.on_message(filters.command(["dsr"], prefix) & filters.me)
async def dsr(client: Client, message: Message):
    db.set("core.antipm", "spamrep", False)
    await message.edit("Spam-reporting disabled")


modules_help.append(
    {
        "antipm": [
            {
                "anti_pm": "Delete all messages from users who are not in the contact book"
            },
            {"disable_anti_pm": "Disable"},
            {"esr": "Enable spam report"},
            {"dsr": "Disable spam report"},
        ]
    }
)
