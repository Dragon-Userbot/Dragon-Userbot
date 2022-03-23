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

import time
from datetime import datetime
from html import escape

from pyrogram import Client, filters
from pyrogram import ContinuePropagation
from pyrogram.errors import RPCError
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from pyrogram.raw.types import UpdateServiceNotification
from pyrogram.types import Message

from utils.db import db
from utils.misc import modules_help, prefix

auth_hashes = db.get("core.sessionkiller", "auths_hashes", [])


@Client.on_message(filters.command(["sessionkiller", "sk"], prefix) & filters.me)
async def sessionkiller(client: Client, message: Message):
    if len(message.command) == 1:
        if db.get("core.sessionkiller", "enabled", False):
            await message.edit(
                "<b>Sessionkiller status: enabled\n"
                f"You can disable it with <code>{prefix}sessionkiller disable</code></b>"
            )
        else:
            await message.edit(
                "<b>Sessionkiller status: disabled\n"
                f"You can enable it with <code>{prefix}sessionkiller enable</code></b>"
            )
    elif message.command[1] in ["enable", "on", "1", "yes", "true"]:
        db.set("core.sessionkiller", "enabled", True)
        await message.edit("<b>Sessionkiller enabled!</b>")

        db.set(
            "core.sessionkiller",
            "auths_hashes",
            [
                auth["hash"]
                for auth in (await client.send(GetAuthorizations()))["authorizations"]
            ],
        )
    elif message.command[1] in ["disable", "off", "0", "no", "false"]:
        db.set("core.sessionkiller", "enabled", False)
        await message.edit("<b>Sessionkiller disabled!</b>")
    else:
        await message.edit(f"<b>Usage: {prefix}sessionkiller [enable|disable]</b>")


@Client.on_raw_update()
async def check_new_login(client: Client, update: UpdateServiceNotification, _, __):
    if not isinstance(update, UpdateServiceNotification) or not update.type.startswith(
        "auth"
    ):
        raise ContinuePropagation
    if not db.get("core.sessionkiller", "enabled", False):
        raise ContinuePropagation
    authorizations = (await client.send(GetAuthorizations()))["authorizations"]
    for auth in authorizations:
        if auth.current:
            continue
        if auth["hash"] not in auth_hashes:
            # found new unexpected login
            try:
                await client.send(ResetAuthorization(hash=auth.hash))
            except RPCError:
                info_text = (
                    "Someone tried to log in to your account. You can see this report because you"
                    "turned on this feature. But I couldn't terminate attacker's session and "
                    "⚠ <b>you must reset it manually</b>. You should change your 2FA password "
                    "(if enabled), or set it.\n"
                )
            else:
                info_text = (
                    "Someone tried to log in to your account. Since you have enabled "
                    "this feature, I deleted the attacker's session from your account. "
                    "You should change your 2FA password (if enabled), or set it.\n"
                )
            logined_time = datetime.utcfromtimestamp(auth.date_created).strftime(
                "%d-%m-%Y %H-%M-%S UTC"
            )
            full_report = (
                "<b>!!! ACTION REQUIRED !!!</b>\n"
                + info_text
                + "Below is the information about the attacker that I got.\n\n"
                f"Unique authorization hash: <code>{auth.hash}</code> (not valid anymore)\n"
                f"Device model: <code>{escape(auth.device_model)}</code>\n"
                f"Platform: <code>{escape(auth.platform)}</code>\n"
                f"API ID: <code>{auth.api_id}</code>\n"
                f"App name: <code>{escape(auth.app_name)}</code>\n"
                f"App version: <code>{auth.app_version}</code>\n"
                f"Logined at: <code>{logined_time}</code>\n"
                f"IP: <code>{auth.ip}</code>\n"
                f"Country: <code>{auth.country}</code>\n"
                f'Official app: <b>{"yes" if auth.official_app else "no"}</b>\n\n'
                f"<b>It is you? Type <code>{prefix}sk off</code> and try logging "
                f"in again.</b>"
            )
            # schedule sending report message so user will get notification
            schedule_date = int(time.time() + 3)
            await client.send_message("me", full_report, schedule_date=schedule_date)
            return


modules_help["sessionkiller"] = {
    "sessionkiller [enable|disable]": "When enabled, every new session will be terminated.\n"
    "Useful for additional protection for your account"
}
