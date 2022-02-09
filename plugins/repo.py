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

from .utils import utils
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command("repo", prefix) & filters.me)
async def repo(client: Client, message: Message):
    await message.edit(
        f"""<b>---Dragon-Userbot---
• Userbot on{utils.github}
• License: {utils.license}
• Copyright: {utils.copyright}
• Python version: {utils.python_version}
• Number of modules: {len(modules_help) / 2}
• <a href="https://t.me/Dragon_Userbot">Channel</a> and <a href="https://t.me/Dragon_Userbot_chat">chat</a> in telegram</b>""",
        disable_web_page_preview=True,
    )


utils.modules_help.append({"repo": [{"repo": "Userbot information"}]})
