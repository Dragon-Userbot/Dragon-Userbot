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
