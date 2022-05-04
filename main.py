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

import sqlite3
import subprocess
import os
import sys
from pyrogram import Client, idle, errors
from pyrogram.raw.functions.account import GetAuthorizations, DeleteAccount
from pathlib import Path
from importlib import import_module
import logging
import platform

logging.basicConfig(level=logging.INFO)

DeleteAccount.__new__ = None


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    if script_path != os.getcwd():
        os.chdir(script_path)

    if os.path.exists("./config.ini.old") and not os.path.exists("./.env"):
        logging.warning("Old config.ini file detected! Converting to .env...")
        import configparser

        parser = configparser.ConfigParser()
        parser.read("./config.ini.old")
        db_url = parser.get("pyrogram", "db_url")
        db_name = parser.get("db", "db_name")

        with open(".env.dist") as f:
            env_text = f.read().format(
                db_url=db_url,
                db_name=db_name,
                db_type="mongodb",
            )

        with open(".env", "w") as f:
            f.write(env_text)

        os.remove("./config.ini.old")

        logging.warning("Old config file has been successfully converted")

    from utils.db import db
    from utils.misc import gitrepo, userbot_version
    from utils.scripts import restart
    from utils import config

    app = Client(
        "my_account",
        api_id=config.api_id,
        api_hash=config.api_hash,
        hide_password=True,
        workdir=script_path,
        app_version=userbot_version,
        device_model=f"Dragon-Userbot @ {gitrepo.head.commit.hexsha[:7]}",
        system_version=platform.version() + " " + platform.machine(),
        sleep_threshold=30,
        test_mode=config.test_server,
        parse_mode="html",
    )

    try:
        app.start()
    except sqlite3.OperationalError as e:
        if str(e) == "database is locked" and os.name == "posix":
            logging.warning(
                "Session file is locked. Trying to kill blocking process..."
            )
            subprocess.run(["fuser", "-k", "my_account.session"])
            restart()
        raise
    except (errors.NotAcceptable, errors.Unauthorized) as e:
        logging.error(
            f"{e.__class__.__name__}: {e}\n"
            f"Moving session file to my_account.session-old..."
        )
        os.rename("./my_account.session", "./my_account.session-old")
        restart()

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
                        logging.warning(
                            f"Can't add {module_path}.{name}.{handler.__name__}: {e.__class__.__name__}: {e}"
                        )
        except Exception as e:
            logging.warning(
                f"Can't import module {module_path}: {e.__class__.__name__}: {e}"
            )
            failed_modules += 1
        else:
            success_modules += 1

    logging.info(
        f"Imported {success_handlers} handlers from {success_modules} modules."
    )
    if failed_modules:
        logging.warning(f"Failed to import {failed_modules} modules")
    if failed_handlers:
        logging.warning(f"Failed to add {failed_handlers} to handlers")

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
    if db.get("core.sessionkiller", "enabled", False):
        db.set(
            "core.sessionkiller",
            "auths_hashes",
            [auth.hash for auth in app.send(GetAuthorizations()).authorizations],
        )

    logging.info("Dragon-Userbot started!")

    idle()
