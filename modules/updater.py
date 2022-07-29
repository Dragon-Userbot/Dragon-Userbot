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
from sys import executable
import sys
import subprocess 
from asyncio import create_subprocess_shell, sleep
from asyncio.subprocess import PIPE

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix, requirements_list
from utils.scripts import format_exc


async def execute(command, pass_error=True):
    """ Executes command and returns output, with the option of enabling stderr. """
    executor = await create_subprocess_shell(
        command,
        stdout=PIPE,
        stderr=PIPE,
        stdin=PIPE
    )

    stdout, stderr = await executor.communicate()
    if pass_error:
        try:
            result = str(stdout.decode().strip()) \
                     + str(stderr.decode().strip())
        except UnicodeDecodeError:
            result = str(stdout.decode('gbk').strip()) \
                     + str(stderr.decode('gbk').strip())
    else:
        try:
            result = str(stdout.decode().strip())
        except UnicodeDecodeError:
            result = str(stdout.decode('gbk').strip())
    return result


def restart(message: Message, restart_type):
    text = "1" if restart_type == "update" else "2"
    os.execvp(
        sys.executable,
        [
            sys.executable,
            "main.py",
            f"{message.chat.id}",
            f" {message.id}",
            f"{text}",
        ],
    )


@Client.on_message(filters.command("restart", prefix) & filters.me)
async def restart_cmd(_, message: Message):
    await message.edit("<b>Restarting...</b>")
    restart(message, "restart")


@Client.on_message(filters.command("update", prefix) & filters.me)
async def update(_, message: Message):
    await message.edit("Please wait...")
    await execute("git fetch --all")
    if len(message.command) > 0:
        await execute("git reset --hard origin/master")
    await execute("git pull --all")
    await execute(f"{executable} -m pip install --upgrade -r requirements.txt")
    await execute(f"{executable} -m pip install -r requirements.txt")
    await message.edit("Update successful")
    restart()
    


modules_help["updater"] = {
    "update": "Update the userbot. If new core modules are avaliable, they will be installed",
    "restart": "Restart userbot",
}
