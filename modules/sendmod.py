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
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import (
    format_exc,
    format_module_help,
    format_small_module_help,
)


@Client.on_message(filters.command(["sendmod", "sm"], prefix) & filters.me)
async def sendmod(client: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("<b>Module name to send is not provided</b>")
        return

    await message.edit("<b>Dispatching...</b>")
    try:
        module_name = message.command[1].lower()
        if module_name in modules_help:
            text = format_module_help(module_name)
            if len(text) >= 1024:
                text = format_small_module_help(module_name)
            if os.path.isfile(f"modules/{module_name}.py"):
                await client.send_document(
                    message.chat.id, f"modules/{module_name}.py", caption=text
                )
            elif os.path.isfile(
                f"modules/custom_modules/{module_name.lower()}.py"
            ):
                await client.send_document(
                    message.chat.id,
                    f"modules/custom_modules/{module_name}.py",
                    caption=text,
                )
            await message.delete()
        else:
            await message.edit(f"<b>Module {module_name} not found!</b>")
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["sendmod"] = {
    "sendmod [module_name]": "Send module to interlocutor",
}
