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

ru_keys = (
    """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё"№;%:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"""
)
en_keys = (
    """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$%^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?"""
)
table = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)


@Client.on_message(filters.command(["switch", "sw"], prefix) & filters.me)
async def switch(client: Client, message: Message):
    if len(message.command) == 1:
        if message.reply_to_message:
            text = message.reply_to_message.text
        else:
            history = await client.get_history(message.chat.id, limit=2)
            if history and history[1].from_user.is_self and history[1].text:
                text = history[1].text
            else:
                await message.edit("<b>Text to switch not found</b>")
                return
    else:
        text = message.text.split(maxsplit=1)[1]

    await message.edit(str.translate(text, table))


modules_help["switch"] = {
    "sw [reply/text for switch]*": "Useful when tou forgot to change the keyboard layout",
}
