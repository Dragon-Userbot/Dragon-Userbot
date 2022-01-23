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
import pathlib

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix, requirements_list
from utils.scripts import format_exc


HOME_FILE_PATH = pathlib.Path.home() / "dragon-userbot-config.ini"
CURRENT_FILE_PATH = pathlib.Path.cwd() / "config.ini"


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
async def restart_cmd(_, message: Message):
    await message.edit("<b>Restarting...</b>")
    await restart(message, "restart")


@Client.on_message(filters.command("update", prefix) & filters.me)
async def update(_, message: Message):
    try:
        await message.edit("<b>Updating: 1/4 (updating pip)</b>")
        subprocess.run(["python3", "-m", "pip", "install", "-U", "pip"])
        await message.edit("<b>Updating: 2/4 (git pull)</b>")
        CURRENT_FILE_PATH.replace(HOME_FILE_PATH)
        subprocess.run(["git", "restore", "config.ini"])
        subprocess.run(["git", "pull"])
        HOME_FILE_PATH.replace(CURRENT_FILE_PATH)
        await message.edit("<b>Updating: 3/4 (updating libs from requirements.txt)</b>")
        subprocess.run(
            ["python3", "-m", "pip", "install", "-U", "-r", "requirements.txt"]
        )
        await message.edit(
            "<b>Updating: 4/4 (updating libs from requirements_list)</b>"
        )
        subprocess.run(["python3", "-m", "pip", "install", "-U", *requirements_list])
        await message.edit("<b>Updating: done! Restarting...</b>")
    except Exception as e:
        await message.edit(format_exc(e))
    else:
        await restart(message, "update")


modules_help["updater"] = {
    "update": "Update the userbot. If new core modules are avaliable, they will be installed",
    "restart": "Restart userbot",
}
