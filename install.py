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

import configparser
import datetime
import os
import sys

from pyrogram import Client

if len(sys.argv) == 2:
    arg = sys.argv[1]
    config_path = os.path.join(sys.path[0], "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    config.set("pyrogram", "db_url", arg)
    with open(config_path, "w") as config_file:
        config.write(config_file)

    app = Client("my_account")
    app.start()
    app.send_message(
        "me",
        f"<b>[{datetime.datetime.now()}] Dragon-Userbot launched! \n"
        f"For restart, enter:</b> \n"
        f"<code>cd Dragon-Userbot/ && python main.py</code>",
    )

    app.stop()

    print("Account is successfully linked, for run use: python main.py")
