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

import os

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions

date_dict = {}


@Client.on_message(filters.chat("@creationdatebot"), group=-1)
async def get_date(client: Client, message: Message):
    await client.read_history("@creationdatebot")
    date_dict.update({"date": message.text})


async def text(client: Client, message: Message):
    if message.text:
        return message.text
    else:
        return message.caption


async def chat_permissions(client: Client, message: Message):
    return ChatPermissions(
        can_send_messages=message.chat.permissions.can_send_messages,
        can_send_media_messages=message.chat.permissions.can_send_media_messages,
        can_send_stickers=message.chat.permissions.can_send_stickers,
        can_send_animations=message.chat.permissions.can_send_animations,
        can_send_games=message.chat.permissions.can_send_games,
        can_use_inline_bots=message.chat.permissions.can_use_inline_bots,
        can_add_web_page_previews=message.chat.permissions.can_add_web_page_previews,
        can_send_polls=message.chat.permissions.can_send_polls,
        can_change_info=message.chat.permissions.can_change_info,
        can_invite_users=message.chat.permissions.can_invite_users,
        can_pin_messages=message.chat.permissions.can_pin_messages,
    )


async def restart():
    await os.execvp("python3", ["python3", "main.py"])
