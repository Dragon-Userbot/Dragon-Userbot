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
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, interact_with, interact_with_to_delete


@Client.on_message(filters.command("info", prefix) & filters.me)
async def get_user_inf(client: Client, message: Message):
    if len(message.command) >= 2:
        peer = message.command[1]
    elif message.reply_to_message and message.reply_to_message.from_user:
        peer = message.reply_to_message.from_user.id
    else:
        peer = "me"

    user = await client.get_users(peer)
    full_user = await client.get_chat(peer)

    if user.username is None:
        username = "None"
    else:
        username = f"@{user.username}"
    about = "None" if full_user.bio is None else full_user.bio

    user_info = f"""|=<b>Username: {username}
|-Id: <code>{user.id}</code>
|-Bot: <code>{user.is_bot}</code>
|-Scam: <code>{user.is_scam}</code>
|-Prem: <code>{user.is_premium}</code>
|-Name: <code>{user.first_name}</code>
|-BIO: <code>{about}</code>
</b>"""
    await message.edit(user_info)


@Client.on_message(filters.command("infofull", prefix) & filters.me)
async def get_full_user_inf(client: Client, message: Message):
    await message.edit("<b>Receiving the information...</b>")

    try:
        if len(message.command) >= 2:
            peer = message.command[1]
        elif message.reply_to_message and message.reply_to_message.from_user:
            peer = message.reply_to_message.from_user.id
        else:
            peer = "me"

        user = await client.get_users(peer)
        full_user = await client.get_chat(peer)

        if user.username is None:
            username = "None"
        else:
            username = f"@{user.username}"
        about = "None" if full_user.bio is None else full_user.bio
        user_info = f"""|=<b>Username: {username}
|-Id: <code>{user.id}</code>
|-Bot: <code>{user.is_bot}</code>
|-Scam: <code>{user.is_scam}</code>
|-Prem: <code>{user.is_premium}</code>
|-Name: <code>{user.first_name}</code>
|-BIO: <code>{about}</code>
|-Contact: <code>{user.is_contact}</code>
|-Can pin message: <code>{full_user.can_pin_message}</code>
|-Mutual contact: <code>{user.is_mutual_contact}</code>
|-Access hash: <code>{user.access_hash}</code>
|-Restricted: <code>{user.is_restricted}</code>
|-Verified: <code>{user.is_verified}</code>
|-Phone calls available: <code>{full_user.phone_calls_available}</code>
|-Phone calls private: <code>{full_user.phone_calls_private}</code>
|-Blocked: <code>{full_user.blocked}</code></b>"""
        await message.edit(user_info)
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["user_info"] = {
    "info [reply|id|username]": "Get brief information about user",
    "infofull [reply|id|username": "Get full information about user",
}
