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

import sys
from pyrogram import Client, idle, errors
from pyrogram.raw.functions.account import GetAuthorizations
from utils.db import db


app = Client("my_account")

if __name__ == "__main__":
    app.start()

    if len(sys.argv) == 4:  # restart initiated by userbot
        restart_type = sys.argv[3]
        if restart_type == "1":
            text = "<b>Update process completed!</b>"
        else:
            text = "<b>Restart completed!</b>"
        try:
            app.send_message(
                chat_id=sys.argv[1],
                text=text,
                reply_to_message_id=int(sys.argv[2]),
            )
        except errors.RPCError:
            app.send_message(chat_id=sys.argv[1], text=text)

    # required by sessionkiller module
    auths = app.send(GetAuthorizations())["authorizations"]
    auth_hashes = [auth["hash"] for auth in auths]
    db.set("core.sessionkiller", "auths_hashes", auth_hashes)

    print("Dragon-Userbot started!")

    idle()
