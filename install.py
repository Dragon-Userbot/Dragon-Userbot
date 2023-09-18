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
import sys
from pyrogram import Client, errors

from utils import config

if __name__ == "__main__":
    app = Client(
        "my_account",
        api_id=config.api_id,
        api_hash=config.api_hash,
        hide_password=True,
        test_mode=config.test_server,
    )

    if config.db_type in ["mongo", "mongodb"]:
        from pymongo import MongoClient, errors

        db = MongoClient(config.db_url)
        try:
            db.server_info()
        except errors.ConnectionFailure as e:
            raise RuntimeError(
                "MongoDB server isn't available! "
                f"Provided url: {config.db_url}. "
                "Enter valid URL and restart installation"
            ) from e

    install_type = sys.argv[1] if len(sys.argv) > 1 else "3"
    if install_type == "1":
        restart = "pm2 restart dragon"
    elif install_type == "2":
        restart = "sudo systemctl restart dragon"
    else:
        restart = "cd Dragon-Userbot/ && python main.py"

    app.start()
    try:
        app.send_message(
            "me",
            f"<b>[{datetime.datetime.now()}] Dragon-Userbot launched! \n"
            "Channel: @Dragon_Userb0t\n"
            "Custom modules: @Dragon_Userb0t_modules\n"
            "Chat [RU]: @Dragon_Userb0t_chat\n"
            f"For restart, enter:</b>\n"
            f"<code>{restart}</code>",
        )
    except errors.RPCError:
        pass
    app.stop()
