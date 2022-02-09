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

from .utils.utils import modules_help, prefix


# packages from PyPi
# import example_1
# import example_2


@Client.on_message(filters.command("example_edit", prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    await message.edit("<code>This is an example module</code>")


@Client.on_message(filters.command("example_send", prefix) & filters.me)
async def example_send(client: Client, message: Message):
    await client.send_message(message.chat.id, "<b>This is an example module</b>")


# This adds instructions for your module
modules_help.append(
    {"example": [{"example_send": "example send"}, {"example_edit": "example edit"}]}
)
# 'module_name': '''comand_1 - description, comand_2 - description''',
#        │          'module_name module': 'Example send: example_send, example_edit\n\n'
#        │                 │        │
#        │                 │        │
#     module_name(only snake_case)  └─ module (here the word 'module' is required)


# If your custom module requires packages from PyPi, write the names of the packages in these functions
# requirements_list.append('example_1')
# requirements_list.append('example_2')
# etc
