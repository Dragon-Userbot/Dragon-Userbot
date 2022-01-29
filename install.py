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

import datetime
from pyrogram import Client
from utils import config

if __name__ == "__main__":
    app = Client(
        "my_account",
        api_id=config.api_id,
        api_hash=config.api_hash,
        hide_password=True,
    )

    app.start()
    app.send_message(
        "me",
        f"<b>[{datetime.datetime.now()}] Dragon-Userbot launched! \n"
        "Channel: @Dragon_Userbot\n"
        "Custom modules: @Dragon_Userbot_modules\n"
        "Chat [RU]: @Dragon_Userbot_chat\n"
        "Chat [EN]: @Dragon_Userbot_chat_en\n\n"
        f"For restart, enter:</b> \n"
        f"<code>cd Dragon-Userbot/ && python main.py</code>",
    )
    app.stop()
