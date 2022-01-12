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

import re
from time import time
from typing import Dict, Union

from pyrogram import Client, ContinuePropagation, filters
from pyrogram.errors import (
    UserAdminInvalid,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameInvalid,
)
from pyrogram.raw import functions, types
from pyrogram.types import Message, ChatPermissions
from pyrogram.utils import (
    get_channel_id,
    MAX_USER_ID,
    MIN_CHAT_ID,
    MAX_CHANNEL_ID,
    MIN_CHANNEL_ID,
)

from .utils.db import db
from .utils.scripts import text, chat_permissions
from .utils.utils import modules_help, prefix


async def check_username_or_id(data: Union[str, int]) -> str:
    data = str(data)
    if (
        not data.isdigit()
        and data[0] == "-"
        and not data[1:].isdigit()
        or not data.isdigit()
        and data[0] != "-"
    ):
        return "channel"
    else:
        peer_id = int(data)
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError(f"Peer id invalid: {peer_id}")


async def get_user_and_name(message):
    if message.reply_to_message.from_user:
        return (
            message.reply_to_message.from_user.id,
            message.reply_to_message.from_user.first_name,
        )
    elif message.reply_to_message.sender_chat:
        return (
            message.reply_to_message.sender_chat.id,
            message.reply_to_message.sender_chat.title,
        )


@Client.on_message()
async def restrict_users_in_tmute(client: Client, message: Message):
    tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
    if (
        message.from_user
        and message.from_user.id in tmuted_users
        or not message.from_user
        and message.sender_chat
        and message.sender_chat.id in tmuted_users
    ):
        await message.delete()
    raise ContinuePropagation


@Client.on_message(filters.command(["ban"], prefix) & filters.me)
async def ban_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        user_for_ban, name = await get_user_and_name(message)
        try:
            await client.ban_chat_member(message.chat.id, user_for_ban)
            channel = await client.resolve_peer(message.chat.id)
            user_id = await client.resolve_peer(user_for_ban)
            if "report_spam" in cause.lower().split():
                await client.send(
                    functions.channels.ReportSpam(
                        channel=(channel),
                        user_id=(user_id),
                        id=[message.reply_to_message.message_id],
                    )
                )
            if "delete_history" in cause.lower().split():
                await client.send(
                    functions.channels.DeleteUserHistory(
                        channel=(channel), user_id=(user_id)
                    )
                )
            text_c = "".join(
                f" {_}"
                for _ in cause.split()
                if _.lower() not in ["delete_history", "report_spam"]
            )

            await message.edit(
                f"<b>{name}</b> <code>banned!</code>"
                + f"\n{'<b>Cause:</b> <i>' + text_c.split(maxsplit=1)[1] + '</i>' if len(text_c.split()) > 1 else ''}"
            )
        except UserAdminInvalid:
            await message.edit("<b>No rights</b>")
        except ChatAdminRequired:
            await message.edit("<b>No rights</b>")
        except Exception as e:
            print(e)
            await message.edit("<b>No rights</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await check_username_or_id(cause.split(" ")[1]) == "channel":
                    user_to_ban = await client.get_chat(cause.split(" ")[1])
                    name = user_to_ban.title
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_ban = await client.get_users(cause.split(" ")[1])
                    name = user_to_ban.first_name
                try:
                    await client.ban_chat_member(message.chat.id, user_to_ban.id)
                    await message.edit(
                        f"<b>{name}</b> <code>banned!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["unban"], prefix) & filters.me)
async def unban_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        user_for_unban, name = await get_user_and_name(message)
        try:
            await client.unban_chat_member(message.chat.id, user_for_unban)
            await message.edit(
                f"<b>{name}</b> <code>unbanned!</code>"
                + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
            )
        except UserAdminInvalid:
            await message.edit("<b>No rights</b>")
        except ChatAdminRequired:
            await message.edit("<b>No rights</b>")
        except Exception as e:
            print(e)
            await message.edit("<b>No rights</b>")

    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await check_username_or_id(cause.split(" ")[1]) == "channel":
                    user_to_unban = await client.get_chat(cause.split(" ")[1])
                    name = user_to_unban.title
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_unban = await client.get_users(cause.split(" ")[1])
                    name = user_to_unban.first_name
                try:
                    await client.unban_chat_member(message.chat.id, user_to_unban.id)
                    await message.edit(
                        f"<b>{name}</b> <code>unbanned!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["kick"], prefix) & filters.me)
async def kick_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.ban_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id
                )
                await client.unban_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id
                )
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(
                    message.reply_to_message.from_user.id
                )
                if "report_spam" in cause.lower().split():
                    await client.send(
                        functions.channels.ReportSpam(
                            channel=(channel),
                            user_id=(user_id),
                            id=[message.reply_to_message.message_id],
                        )
                    )
                if "delete_history" in cause.lower().split():
                    await client.send(
                        functions.channels.DeleteUserHistory(
                            channel=(channel), user_id=(user_id)
                        )
                    )
                text_c = "".join(
                    f" {_}"
                    for _ in cause.split()
                    if _.lower() not in ["delete_history", "report_spam"]
                )

                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>kicked!</code>"
                    + f"\n{'<b>Cause:</b> <i>' + text_c.split(maxsplit=1)[1] + '</i>' if len(text_c.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_ban = await client.get_users(cause.split(" ")[1])
                try:
                    await client.ban_chat_member(message.chat.id, user_to_ban.id)
                    await client.unban_chat_member(message.chat.id, user_to_ban.id)
                    await message.edit(
                        f"<b>{user_to_ban.first_name}</b> <code>kicked!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tmute"], prefix) & filters.me)
async def tmute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        user_for_tmute, name = await get_user_and_name(message)

        if message.reply_to_message.from_user.is_self:
            return await message.edit("<b>Not on yourself</b>")

        tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
        if user_for_tmute not in tmuted_users:
            tmuted_users.append(user_for_tmute)
            db.set("core.ats", f"c{message.chat.id}", tmuted_users)
            await message.edit(
                f"<b>{name}</b> <code>in tmute</code>"
                + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
            )
        else:
            await message.edit(f"<b>{name}</b> <code>already in tmute</code>")

    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await check_username_or_id(cause.split(" ")[1]) == "channel":
                    user_to_tmute = await client.get_chat(cause.split(" ")[1])
                    name = user_to_tmute.title
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_tmute = await client.get_users(cause.split(" ")[1])
                    name = user_to_tmute.first_name
                    if user_to_tmute.is_self:
                        return await message.edit("<b>Not on yourself</b>")

                tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                if user_to_tmute.id not in tmuted_users:
                    tmuted_users.append(user_to_tmute.id)
                    db.set("core.ats", f"c{message.chat.id}", tmuted_users)
                    await message.edit(
                        f"<b>{name}</b> <code>in tmute</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                else:
                    await message.edit(f"<b>{name}</b> <code>already in tmute</code>")

            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tunmute"], prefix) & filters.me)
async def tunmute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:

        user_for_tunmute, name = await get_user_and_name(message)

        if message.reply_to_message.from_user.is_self:
            return await message.edit("<b>Not on yourself</b>")

        tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
        if user_for_tunmute not in tmuted_users:
            await message.edit(f"<b>{name}</b> <code>not in tmute</code>")
        else:
            tmuted_users.remove(user_for_tunmute)
            db.set("core.ats", f"c{message.chat.id}", tmuted_users)
            await message.edit(
                f"<b>{name}</b> <code>tunmuted</code>"
                + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
            )

    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await check_username_or_id(cause.split(" ")[1]) == "channel":
                    user_to_tunmute = await client.get_chat(cause.split(" ")[1])
                    name = user_to_tunmute.title
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_tunmute = await client.get_users(cause.split(" ")[1])
                    name = user_to_tunmute.first_name
                    if user_to_tunmute.is_self:
                        return await message.edit("<b>Not on yourself</b>")

                tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                if user_to_tunmute.id not in tmuted_users:
                    await message.edit(f"<b>{name}</b> <code>not in tmute</code>")
                else:
                    tmuted_users.remove(user_to_tunmute.id)
                    db.set("core.ats", f"c{message.chat.id}", tmuted_users)
                    await message.edit(
                        f"<b>{name}</b> <code>tunmuted</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tmute_users"], prefix) & filters.me)
async def tunmute_users_command(client: Client, message: Message):
    if message.chat.type not in ["private", "channel"]:
        text = f"<b>All users</b> <code>{message.chat.title}</code> <b>who are now in tmute</b>\n\n"
        count = 0
        tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
        for user in tmuted_users:
            try:
                _name_ = await client.get_chat(user)
                count += 1
                if await check_username_or_id(_name_.id) == "channel":
                    channel = await client.send(
                        functions.channels.GetChannels(
                            id=[
                                types.InputChannel(
                                    channel_id=get_channel_id(_name_.id),
                                    access_hash=0,
                                )
                            ]
                        )
                    )
                    name = channel.chats[0].title
                elif await check_username_or_id(_name_.id) == "user":
                    user = await client.get_users(_name_.id)
                    name = user.first_name
                text += f"{count}. <b>{name}</b>\n"
            except PeerIdInvalid:
                pass
        if count == 0:
            await message.edit("<b>No users in tmute</b>")
        else:
            text += f"\n<b>Total users in tmute</b> {count}"
            await message.edit(text)
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["unmute"], prefix) & filters.me)
async def unmute_command(client, message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        u_p = await chat_permissions(client, message)
        if message.reply_to_message.from_user:
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    u_p,
                    int(time() + 30),
                )
                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>unmuted</code>"
                    + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        u_p = await chat_permissions(client, message)
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                try:
                    await client.restrict_chat_member(
                        message.chat.id, user_to_unmute.id, u_p, int(time() + 30)
                    )
                    await message.edit(
                        f"<b>{user_to_unmute.first_name}</b> <code>unmuted!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["mute"], prefix) & filters.me)
async def mute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        mute_seconds: int = 0
        for character in "mhdw":
            match = re.search(rf"(\d+|(\d+\.\d+)){character}", message.text)
            if match:
                if character == "m":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1]) * 60 // 1
                    )
                if character == "h":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1]) * 3600 // 1
                    )
                if character == "d":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 86400
                        // 1
                    )
                if character == "w":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 604800
                        // 1
                    )
        try:
            if mute_seconds > 30:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    ChatPermissions(),
                    int(time()) + mute_seconds,
                )
                from_user = message.reply_to_message.from_user
                mute_time: Dict[str, int] = {
                    "days": mute_seconds // 86400,
                    "hours": mute_seconds % 86400 // 3600,
                    "minutes": mute_seconds % 86400 % 3600 // 60,
                }
                message_text = (
                    f"<b>{from_user.first_name}</b> <code> was muted for"
                    f" {((str(mute_time['days']) + ' day') if mute_time['days'] > 0 else '') + ('s' if mute_time['days'] > 1 else '')}"
                    f" {((str(mute_time['hours']) + ' hour') if mute_time['hours'] > 0 else '') + ('s' if mute_time['hours'] > 1 else '')}"
                    f" {((str(mute_time['minutes']) + ' minute') if mute_time['minutes'] > 0 else '') + ('s' if mute_time['minutes'] > 1 else '')}</code>"
                    + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                )
                while "  " in message_text:
                    message_text = message_text.replace("  ", " ")
            else:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    ChatPermissions(),
                )
                message_text = (
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code> was muted for never</code>"
                    + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            await message.edit(message_text)
        except UserAdminInvalid:
            await message.edit("<b>No rights</b>")
        except ChatAdminRequired:
            await message.edit("<b>No rights</b>")
        except Exception as e:
            print(e)
            await message.edit("<b>No rights</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                mute_seconds: int = 0
                for character in "mhdw":
                    match = re.search(rf"(\d+|(\d+\.\d+)){character}", message.text)
                    if match:
                        if character == "m":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 60
                                // 1
                            )
                        if character == "h":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 3600
                                // 1
                            )
                        if character == "d":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 86400
                                // 1
                            )
                        if character == "w":
                            mute_seconds += int(
                                float(match.string[match.start() : match.end() - 1])
                                * 604800
                                // 1
                            )
                try:
                    if mute_seconds > 30:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions(),
                            int(time()) + mute_seconds,
                        )
                        mute_time: Dict[str, int] = {
                            "days": mute_seconds // 86400,
                            "hours": mute_seconds % 86400 // 3600,
                            "minutes": mute_seconds % 86400 % 3600 // 60,
                        }
                        message_text = (
                            f"<b>{user_to_unmute.first_name}</b> <code> was muted for"
                            f" {((str(mute_time['days']) + ' day') if mute_time['days'] > 0 else '') + ('s' if mute_time['days'] > 1 else '')}"
                            f" {((str(mute_time['hours']) + ' hour') if mute_time['hours'] > 0 else '') + ('s' if mute_time['hours'] > 1 else '')}"
                            f" {((str(mute_time['minutes']) + ' minute') if mute_time['minutes'] > 0 else '') + ('s' if mute_time['minutes'] > 1 else '')}</code>"
                            + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=3)[3] + '</i>' if len(cause.split()) > 3 else ''}"
                        )
                        while "  " in message_text:
                            message_text = message_text.replace("  ", " ")
                    else:
                        await client.restrict_chat_member(
                            message.chat.id, user_to_unmute.id, ChatPermissions()
                        )
                        message_text = (
                            f"<b>{user_to_unmute.first_name}</b> <code> was muted for never</code>"
                            + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                        )
                    await message.edit(message_text)
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["demote"], prefix) & filters.me)
async def demote_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    is_anonymous=False,
                    can_manage_chat=False,
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_voice_chats=False,
                )
                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>demoted!</code>"
                    + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(
                        message.chat.id,
                        promote_user.id,
                        is_anonymous=False,
                        can_manage_chat=False,
                        can_change_info=False,
                        can_post_messages=False,
                        can_edit_messages=False,
                        can_delete_messages=False,
                        can_restrict_members=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                        can_manage_voice_chats=False,
                    )
                    await message.edit(
                        f"<b>{promote_user.first_name}</b> <code>demoted!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["promote"], prefix) & filters.me)
async def promote_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                )
                if len(cause.split()) > 1:
                    await client.set_administrator_title(
                        message.chat.id,
                        message.reply_to_message.from_user.id,
                        cause.split(maxsplit=1)[1],
                    )
                await message.edit(
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code>promoted!</code>"
                    + f"\n{'<b>Prefix:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(
                        message.chat.id,
                        promote_user.id,
                        can_delete_messages=True,
                        can_restrict_members=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    )
                    if len(cause.split()) > 1:
                        await client.set_administrator_title(
                            message.chat.id,
                            promote_user.id,
                            f"\n{cause.split(' ', maxsplit=2)[2] if len(cause.split()) > 2 else None}",
                        )
                    await message.edit(
                        f"<b>{promote_user.first_name}</b> <code>promoted!</code>"
                        + f"\n{'<b>Prefix:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    else:
        await message.edit("<b>Unsupported</b>")


modules_help.append(
    {
        "admintool": [
            {
                "ban [reply]/[username/id]* [reason] [report_spam] [delete_history]": "ban user/channel in chat"
            },
            {
                "unban [reply]/[username/id]* [reason] [report_spam] [delete_history]": "unban user/channel in chat"
            },
            {
                "kick [reply]/[userid]* [reason] [report_spam] [delete_history]": "kick user out of chat"
            },
            {
                "tmute [reply]/[username/id]* [reason]": "delete all new messages from user/channel in chat"
            },
            {
                "tunmute [reply]/[username/id]* [reason]": "stop deleting all new messages from user/channel in chat"
            },
            {
                "tmute_users": "cheklist all users/channel, whose messages will be deleted in chat"
            },
            {
                "mute [reply]/[userid]* [reason] [1m]/[1h]/[1d]/[1w]": "mute user in chat"
            },
            {"unmute [reply]/[userid]* [reason]": "unmute user in chat"},
            {"promote [reply]/[userid]* [prefix]": "promote user in chat"},
            {"demote [reply]/[userid]* [reason]": "demote user in chat"},
        ]
    }
)
