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
from pathlib import Path
from importlib import import_module

from utils.db import db

app = Client("my_account")

if __name__ == "__main__":
    app.start()

    success_handlers = 0
    failed_handlers = 0
    success_modules = 0
    failed_modules = 0

    for path in sorted((Path("modules")).rglob("*.py")):
        module_path = ".".join(path.parent.parts + (path.stem,))
        try:
            module = import_module(module_path)
            for name, obj in vars(module).items():
                # defaulting to [] if obj isn't a function-handler
                for handler, group in getattr(obj, "handlers", []):
                    try:
                        app.add_handler(handler, group)
                        success_handlers += 1
                    except Exception as e:
                        failed_handlers += 1
                        print(
                            f"Can't add {module_path}.{name}.{handler.__name__}: {e.__class__.__name__}: {e}"
                        )
        except Exception as e:
            print(f"Can't import module {module_path}: {e.__class__.__name__}: {e}")
            failed_modules += 1
        else:
            success_modules += 1

    print(f"Imported {success_handlers} handlers from {success_modules} modules.")
    if failed_modules:
        print(f"Failed to import {failed_modules} modules")
    if failed_handlers:
        print(f"Failed to add {failed_handlers} to handlers")

    if len(sys.argv) == 4:
        restart_type = sys.argv[3]
        if restart_type == "1":
            text = "<b>Update process completed!</b>"
        else:
            text = "<b>Restart completed!</b>"
        try:
            app.send_message(
                chat_id=sys.argv[1], text=text, reply_to_message_id=int(sys.argv[2])
            )
        except errors.RPCError:
            app.send_message(chat_id=sys.argv[1], text=text)

    # required for sessionkiller module
    auths = app.send(GetAuthorizations())["authorizations"]
    auth_hashes = [auth["hash"] for auth in auths]
    db.set("core.sessionkiller", "auths_hashes", auth_hashes)

    print("Dragon-Userbot started!")

    idle()
