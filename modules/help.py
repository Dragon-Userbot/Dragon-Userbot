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
from utils.scripts import format_module_help


@Client.on_message(filters.command(["help", "h"], prefix) & filters.me)
async def help_cmd(_, message: Message):
    if len(message.command) == 1:
        msg_edited = False
        text = (
            "<b>Help for <a href=https://t.me/Dragon_Userbot_chat>Dragon-Userbot</a>\n"
            f"For more help on how to use a command, type <code>{prefix}help [module]</code>\n\n"
            "Available Modules:\n"
        )

        for module_name, module_commands in modules_help.items():
            text += "• {}: {}\n".format(
                module_name.title(),
                " ".join(
                    [
                        f"<code>{prefix + cmd_name.split()[0]}</code>"
                        for cmd_name in module_commands.keys()
                    ]
                ),
            )
            if len(text) >= 2048:
                text += "</b>"
                if msg_edited:
                    await message.reply(text, disable_web_page_preview=True)
                else:
                    await message.edit(text, disable_web_page_preview=True)
                    msg_edited = True
                text = "<b>"

        text += f"\nThe number of modules in the userbot: {len(modules_help) / 1}</b>"

        if msg_edited:
            await message.reply(text, disable_web_page_preview=True)
        else:
            await message.edit(text, disable_web_page_preview=True)
    else:
        module_name = message.text.split(maxsplit=1)[1].lower()
        if module_name in modules_help:
            await message.edit(format_module_help(module_name))
        else:
            await message.edit(f"<b>Module {module_name} not found</b>")


modules_help["help"] = {
    "help [module name]": "To get help. Module name isn't required."
}
