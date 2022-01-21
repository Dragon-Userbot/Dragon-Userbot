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

from utils.misc import modules_help, prefix


@Client.on_message(filters.command(["google", "g"], prefix) & filters.me)
async def webshot(client: Client, message: Message):
    user_request = " ".join(message.command[1:])

    if user_request == "":
        if message.reply_to_message:
            reply_user_request = message.reply_to_message.text
            request = reply_user_request.replace(" ", "+")
            full_request = f"https://lmgtfy.app/?s=g&iie=1&q={request}"
            await message.edit(
                f"<a href={full_request}>{reply_user_request}</a>",
                disable_web_page_preview=True,
            )

    else:
        request = user_request.replace(" ", "+")
        full_request = f"https://lmgtfy.app/?s=g&iie=1&q={request}"
        await message.edit(
            f"<a href={full_request}>{user_request}</a>", disable_web_page_preview=True
        )


modules_help.append(
    {
        "google": [
            {
                "google [request]": "To teach the interlocutor to use Google. Request isn't required."
            }
        ]
    }
)
