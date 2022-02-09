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
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message

from .utils.utils import modules_help, prefix
from .utils.utils import requirements_list


async def restart(message: Message, restart_type):
    text = "1" if restart_type == "update" else "2"
    await os.execvp(
        "python3",
        [
            "python3",
            "main.py",
            f"{message.chat.id}",
            f" {message.message_id}",
            f"{text}",
        ],
    )


@Client.on_message(filters.command("restart", prefix) & filters.me)
async def restart_comand(client: Client, message: Message):
    await message.edit("<code>Restarting...</code>")
    await restart(message, restart_type="restart")


@Client.on_message(filters.command("update", prefix) & filters.me)
async def update(client: Client, message: Message):
    await message.edit("<code>Updating...</code>")
    pip_update = subprocess.Popen(
        ["python3", "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.PIPE
    )
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)
    for lib in range(len(requirements_list)):
        process = subprocess.Popen(
            ["pip3", "install", "-U", f"{requirements_list[lib]}"],
            stdout=subprocess.PIPE,
        )
        output = process.communicate()[0]
        print(output)
    await message.edit("<code>Restarting...</code>")
    await restart(message, restart_type="update")


modules_help.append(
    {
        "updater": [
            {
                "update": "Updating the userbot. If new modules are available，they will be installed"
            },
            {"restart": "Restart userbot"},
        ]
    }
)
