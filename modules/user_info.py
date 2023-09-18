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


@Client.on_message(filters.command("inf", prefix) & filters.me)
async def get_user_inf(client: Client, message: Message):
    if len(message.command) >= 2:
        peer = await client.resolve_peer(message.command[1])
    elif message.reply_to_message and message.reply_to_message.from_user:
        peer = await client.resolve_peer(message.reply_to_message.from_user.id)
    else:
        peer = await client.resolve_peer("me")

    response = await client.invoke(functions.users.GetFullUser(id=peer))

    user = response.users[0]
    full_user = response.full_user

    if user.username is None:
        username = "None"
    else:
        username = f"@{user.username}"
    about = "None" if full_user.about is None else full_user.about

    user_info = f"""|=<b>Username: {username}
|-Id: <code>{user.id}</code>
|-Bot: <code>{user.bot}</code>
|-Scam: <code>{user.scam}</code>
|-Name: <code>{user.first_name}</code>
|-Deleted: <code>{user.deleted}</code>
|-BIO: <code>{about}</code>
</b>"""
    await message.edit(user_info)


@Client.on_message(filters.command("inffull", prefix) & filters.me)
async def get_full_user_inf(client: Client, message: Message):
    await message.edit("<b>Receiving the information...</b>")

    try:
        if len(message.command) >= 2:
            peer = await client.resolve_peer(message.command[1])
        elif message.reply_to_message and message.reply_to_message.from_user:
            peer = await client.resolve_peer(
                message.reply_to_message.from_user.id
            )
        else:
            peer = await client.resolve_peer("me")

        response = await client.invoke(functions.users.GetFullUser(id=peer))

        user = response.users[0]
        full_user = response.full_user

        await client.unblock_user("@creationdatebot")
        try:
            response = await interact_with(
                await client.send_message("creationdatebot", f"/id {user.id}")
            )
        except RuntimeError:
            creation_date = "None"
        else:
            creation_date = response.text
        await client.delete_messages(
            "@creationdatebot", interact_with_to_delete
        )
        interact_with_to_delete.clear()

        if user.username is None:
            username = "None"
        else:
            username = f"@{user.username}"
        about = "None" if full_user.about is None else full_user.about
        user_info = f"""|=<b>Username: {username}
|-Id: <code>{user.id}</code>
|-Account creation date: <code>{creation_date}</code>
|-Bot: <code>{user.bot}</code>
|-Scam: <code>{user.scam}</code>
|-Name: <code>{user.first_name}</code>
|-Deleted: <code>{user.deleted}</code>
|-BIO: <code>{about}</code>
|-Contact: <code>{user.contact}</code>
|-Can pin message: <code>{full_user.can_pin_message}</code>
|-Mutual contact: <code>{user.mutual_contact}</code>
|-Access hash: <code>{user.access_hash}</code>
|-Restricted: <code>{user.restricted}</code>
|-Verified: <code>{user.verified}</code>
|-Phone calls available: <code>{full_user.phone_calls_available}</code>
|-Phone calls private: <code>{full_user.phone_calls_private}</code>
|-Blocked: <code>{full_user.blocked}</code></b>"""
        await message.edit(user_info)
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["user_info"] = {
    "inf [reply|id|username]": "Get brief information about user",
    "inffull [reply|id|username": "Get full information about user",
}
