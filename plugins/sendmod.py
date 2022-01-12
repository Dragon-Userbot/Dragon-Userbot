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

import asyncio
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from .utils.utils import modules_help, prefix


@Client.on_message(filters.command(["sendmod", "sm"], prefix) & filters.me)
async def sendmod(client: Client, message: Message):
    module_name = message.command[1]
    try:
        await message.edit("<code>Dispatch...</code>")
        text = f"<b>Help for <i>{module_name}</i>\n\nUsage:</b>\n"
        found = False
        for mh in modules_help:
            if list(mh.keys())[0].lower() == module_name.lower():
                found = True
                cmds = list(mh.values()).pop(0)
                for u_cmd in cmds:
                    cmd = list(u_cmd.items())[0]
                    text += f"""<code>{prefix + cmd[0]}</code> - <i>{cmd[1]}</i>\n"""
        if not found:
            text = "<b>Module <i>{module_name}</i> not found!</b>"

        if os.path.isfile(f"plugins/{module_name.lower()}.py"):
            await client.send_document(
                message.chat.id, f"plugins/{module_name.lower()}.py", caption=text
            )
        elif os.path.isfile(f"plugins/custom_modules/{module_name.lower()}.py"):
            await client.send_document(
                message.chat.id,
                f"plugins/custom_modules/{module_name.lower()}.py",
                caption=text,
            )
        await message.delete()
    except:
        await message.edit("<b>Invalid module name!</b>")
        await asyncio.sleep(5)
        await message.delete()


modules_help.append(
    {
        "sendmod": [
            {"sendmod [module name]*": "Send one of the modules to the interlocutor"}
        ]
    }
)
