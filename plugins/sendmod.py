from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw import types, functions
from .utils.utils import modules_help, prefix
from .utils.help_formatting import help_formatting
import os

import asyncio


@Client.on_message(filters.command(["sendmod", "sm"], prefix) & filters.me)
async def sendmod(client: Client, message: Message):
    mod_name = message.command[1]
    try:
        await message.edit("<code>Dispatch...</code>")
        text = help_formatting(
            modules_help[mod_name.lower()],
            help_type="one_mod",
            module_name=mod_name.lower(),
        )
        if os.path.isfile(f"plugins/{mod_name}.py"):
            await client.send_document(
                message.chat.id, f"plugins/{mod_name}.py", caption=text
            )
        elif os.path.isfile(f"plugins/custom_modules/{mod_name}.py"):
            await client.send_document(
                message.chat.id, f"plugins/custom_modules/{mod_name}.py", caption=text
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
