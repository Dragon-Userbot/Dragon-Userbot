from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import config, config_path, modules_help, prefix
from .utils.scripts import restart
from .utils.db import db


@Client.on_message(
    filters.command(["sp", "setprefix", "setprefix_dragon"], prefix) & filters.me
)
async def pref(client: Client, message: Message):
    if len(message.command) > 1:
        prefix = message.command[1]
        print(message.command)
        db.set("core.main", "prefix", prefix)
        await message.edit(f"<b>Prefix [ <code>{prefix}</code> ] is set!</b>")
        await restart()
    else:
        await message.edit("<b>The prefix must not be empty!</b>")


modules_help.append(
    {
        "prefix": [
            {"setprefix [prefix]*": "Set custom prefix"},
            {"setprefix_dragon [prefix]*": "Set custom prefix"},
        ]
    }
)
