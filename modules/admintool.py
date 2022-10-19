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
from datetime import timedelta, datetime
from time import time
from typing import Dict, Union
from contextlib import suppress

from pyrogram import Client, ContinuePropagation, filters
from pyrogram.errors import (
    UserAdminInvalid,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameInvalid,
    RPCError,
)
from pyrogram.raw import functions, types
from pyrogram.types import Message, ChatPermissions, ChatPrivileges
from pyrogram.utils import (
    get_channel_id,
    MAX_USER_ID,
    MIN_CHAT_ID,
    MAX_CHANNEL_ID,
    MIN_CHANNEL_ID,
)

from utils.db import db
from utils.scripts import text, format_exc, with_reply
from utils.misc import modules_help, prefix


db_cache: dict = db.get_collection("core.ats")


def update_cache():
    db_cache.clear()
    db_cache.update(db.get_collection("core.ats"))


@Client.on_message(filters.group & ~filters.me)
async def admintool_handler(_, message: Message):
    if message.sender_chat:
        if (
            message.sender_chat.type == "supergroup"
            or message.sender_chat.id
            == db_cache.get(f"linked{message.chat.id}", 0)
        ):
            raise ContinuePropagation

    if message.sender_chat and db_cache.get(f"antich{message.chat.id}", False):
        with suppress(RPCError):
            await message.delete()
            await message.chat.ban_member(message.sender_chat.id)

    tmuted_users = db_cache.get(f"c{message.chat.id}", [])
    if (
        message.from_user
        and message.from_user.id in tmuted_users
        or message.sender_chat
        and message.sender_chat.id in tmuted_users
    ):
        with suppress(RPCError):
            await message.delete()

    if db_cache.get(f"antiraid{message.chat.id}", False):
        with suppress(RPCError):
            await message.delete()
            if message.from_user:
                await message.chat.ban_member(message.from_user.id)
            elif message.sender_chat:
                await message.chat.ban_member(message.sender_chat.id)

    if message.new_chat_members:
        if db_cache.get(f"welcome_enabled{message.chat.id}", False):
            await message.reply(
                db_cache.get(f"welcome_text{message.chat.id}"),
                disable_web_page_preview=True,
            )

    raise ContinuePropagation


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


@Client.on_message(filters.command(["ban"], prefix) & filters.me)
async def ban_command(client: Client, message: Message):
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        user_for_ban, name = await get_user_and_name(message)
        try:
            await client.ban_chat_member(message.chat.id, user_for_ban)
            channel = await client.resolve_peer(message.chat.id)
            user_id = await client.resolve_peer(user_for_ban)
            if "report_spam" in cause.lower().split():
                await client.invoke(
                    functions.channels.ReportSpam(
                        channel=channel,
                        participant=user_id,
                        id=[message.reply_to_message.id],
                    )
                )
            if "delete_history" in cause.lower().split():
                await client.invoke(
                    functions.channels.DeleteParticipantHistory(
                        channel=channel, participant=user_id
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
            await message.edit(format_exc(e))
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await check_username_or_id(cause.split(" ")[1]) == "channel":
                    user_to_ban = await client.get_chat(cause.split(" ")[1])
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_ban = await client.get_users(cause.split(" ")[1])
                else:
                    await message.edit("<b>Invalid user type</b>")
                    return

                name = (
                    user_to_ban.first_name
                    if getattr(user_to_ban, "first_name", None)
                    else user_to_ban.title
                )

                try:
                    channel = await client.resolve_peer(message.chat.id)
                    user_id = await client.resolve_peer(user_to_ban.id)
                    if (
                        "report_spam" in cause.lower().split()
                        and message.reply_to_message
                    ):
                        await client.invoke(
                            functions.channels.ReportSpam(
                                channel=channel,
                                participant=user_id,
                                id=[message.reply_to_message.id],
                            )
                        )
                    if "delete_history" in cause.lower().split():
                        await client.invoke(
                            functions.channels.DeleteParticipantHistory(
                                channel=channel, participant=user_id
                            )
                        )

                    text_c = "".join(
                        f" {_}"
                        for _ in cause.split()
                        if _.lower() not in ["delete_history", "report_spam"]
                    )

                    await client.ban_chat_member(
                        message.chat.id, user_to_ban.id
                    )
                    await message.edit(
                        f"<b>{name}</b> <code>banned!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + text_c.split(' ', maxsplit=2)[2] + '</i>' if len(text_c.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    await message.edit(format_exc(e))
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
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
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
            await message.edit(format_exc(e))

    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await check_username_or_id(cause.split(" ")[1]) == "channel":
                    user_to_unban = await client.get_chat(cause.split(" ")[1])
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_unban = await client.get_users(cause.split(" ")[1])
                else:
                    await message.edit("<b>Invalid user type</b>")
                    return

                name = (
                    user_to_unban.first_name
                    if getattr(user_to_unban, "first_name", None)
                    else user_to_unban.title
                )

                try:
                    await client.unban_chat_member(
                        message.chat.id, user_to_unban.id
                    )
                    await message.edit(
                        f"<b>{name}</b> <code>unbanned!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    await message.edit(format_exc(e))
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
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                await client.ban_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    datetime.now() + timedelta(minutes=1),
                )
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(
                    message.reply_to_message.from_user.id
                )
                if (
                    "report_spam" in cause.lower().split()
                    and message.reply_to_message
                ):
                    await client.invoke(
                        functions.channels.ReportSpam(
                            channel=channel,
                            participant=user_id,
                            id=[message.reply_to_message.id],
                        )
                    )
                if "delete_history" in cause.lower().split():
                    await client.invoke(
                        functions.channels.DeleteParticipantHistory(
                            channel=channel, participant=user_id
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
                await message.edit(format_exc(e))
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
                    channel = await client.resolve_peer(message.chat.id)
                    user_id = await client.resolve_peer(user_to_ban.id)
                    if (
                        "report_spam" in cause.lower().split()
                        and message.reply_to_message
                    ):
                        await client.invoke(
                            functions.channels.ReportSpam(
                                channel=channel,
                                participant=user_id,
                                id=[message.reply_to_message.id],
                            )
                        )
                    if "delete_history" in cause.lower().split():
                        await client.invoke(
                            functions.channels.DeleteParticipantHistory(
                                channel=channel, participant=user_id
                            )
                        )

                    text_c = "".join(
                        f" {_}"
                        for _ in cause.split()
                        if _.lower() not in ["delete_history", "report_spam"]
                    )

                    await client.ban_chat_member(
                        message.chat.id,
                        user_to_ban.id,
                        datetime.now() + timedelta(minutes=1),
                    )
                    await message.edit(
                        f"<b>{user_to_ban.first_name}</b> <code>kicked!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + text_c.split(' ', maxsplit=2)[2] + '</i>' if len(text_c.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    await message.edit(format_exc(e))
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


@Client.on_message(filters.command(["kickdel"], prefix) & filters.me)
async def kickdel_cmd(client: Client, message: Message):
    await message.edit("<b>Kicking deleted accounts...</b>")
    try:
        values = [
            await message.chat.ban_member(
                member.user.id, datetime.now() + timedelta(seconds=31)
            )
            async for member in client.get_chat_members(message.chat.id)
            if member.user.is_deleted
        ]
    except Exception as e:
        return await message.edit(format_exc(e))
    await message.edit(
        f"<b>Successfully kicked {len(values)} deleted account(s)</b>"
    )


@Client.on_message(filters.command(["tmute"], prefix) & filters.me)
async def tmute_command(client: Client, message: Message):
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        user_for_tmute, name = await get_user_and_name(message)

        if (
            message.reply_to_message.from_user
            and message.reply_to_message.from_user.is_self
        ):
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
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_tmute = await client.get_users(cause.split(" ")[1])
                    if user_to_tmute.is_self:
                        return await message.edit("<b>Not on yourself</b>")
                else:
                    await message.edit("<b>Invalid user type</b>")
                    return

                name = (
                    user_to_tmute.first_name
                    if getattr(user_to_tmute, "first_name", None)
                    else user_to_tmute.title
                )

                tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                if user_to_tmute.id not in tmuted_users:
                    tmuted_users.append(user_to_tmute.id)
                    db.set("core.ats", f"c{message.chat.id}", tmuted_users)
                    await message.edit(
                        f"<b>{name}</b> <code>in tmute</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                else:
                    await message.edit(
                        f"<b>{name}</b> <code>already in tmute</code>"
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

    update_cache()


@Client.on_message(filters.command(["tunmute"], prefix) & filters.me)
async def tunmute_command(client: Client, message: Message):
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        user_for_tunmute, name = await get_user_and_name(message)

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
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_tunmute = await client.get_users(
                        cause.split(" ")[1]
                    )
                    if user_to_tunmute.is_self:
                        return await message.edit("<b>Not on yourself</b>")
                else:
                    await message.edit("<b>Invalid user type</b>")
                    return

                name = (
                    user_to_tunmute.first_name
                    if getattr(user_to_tunmute, "first_name", None)
                    else user_to_tunmute.title
                )

                tmuted_users = db.get("core.ats", f"c{message.chat.id}", [])
                if user_to_tunmute.id not in tmuted_users:
                    await message.edit(
                        f"<b>{name}</b> <code>not in tmute</code>"
                    )
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

    update_cache()


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
                    channel = await client.invoke(
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
                else:
                    # invalid user type
                    continue
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
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        u_p = message.chat.permissions
        if message.reply_to_message.from_user:
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    u_p,
                    datetime.now() + timedelta(seconds=30),
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
                await message.edit(format_exc(e))
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        u_p = message.chat.permissions
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                try:
                    await client.restrict_chat_member(
                        message.chat.id,
                        user_to_unmute.id,
                        u_p,
                        datetime.now() + timedelta(seconds=30),
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
                    await message.edit(format_exc(e))
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
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
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
                    message.reply_to_message.from_user.id,
                    ChatPermissions(),
                    datetime.now() + timedelta(seconds=mute_seconds),
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
                    f"<b>{message.reply_to_message.from_user.first_name}</b> <code> was muted indefinitely</code>"
                    + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            await message.edit(message_text)
        except UserAdminInvalid:
            await message.edit("<b>No rights</b>")
        except ChatAdminRequired:
            await message.edit("<b>No rights</b>")
        except Exception as e:
            await message.edit(format_exc(e))
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                mute_seconds: int = 0
                for character in "mhdw":
                    match = re.search(
                        rf"(\d+|(\d+\.\d+)){character}", message.text
                    )
                    if match:
                        if character == "m":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 60
                                // 1
                            )
                        if character == "h":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 3600
                                // 1
                            )
                        if character == "d":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 86400
                                // 1
                            )
                        if character == "w":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 604800
                                // 1
                            )
                try:
                    if mute_seconds > 30:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions(),
                            datetime.now() + timedelta(seconds=mute_seconds),
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
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions(),
                        )
                        message_text = (
                            f"<b>{user_to_unmute.first_name}</b> <code> was muted indefinitely</code>"
                            + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                        )
                    await message.edit(message_text)
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    await message.edit(format_exc(e))
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
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    privileges=ChatPrivileges(
                        is_anonymous=False,
                        can_manage_chat=False,
                        can_change_info=False,
                        can_post_messages=False,
                        can_edit_messages=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    ),
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
                await message.edit(format_exc(e))
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
                        privileges=ChatPrivileges(
                            is_anonymous=False,
                            can_manage_chat=False,
                            can_change_info=False,
                            can_post_messages=False,
                            can_edit_messages=False,
                            can_delete_messages=False,
                            can_manage_video_chats=False,
                            can_restrict_members=False,
                            can_invite_users=False,
                            can_pin_messages=False,
                            can_promote_members=False,
                        ),
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
                    await message.edit(format_exc(e))
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
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    privileges=ChatPrivileges(
                        can_delete_messages=True,
                        can_restrict_members=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    ),
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
                await message.edit(format_exc(e))
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
                        privileges=ChatPrivileges(
                            can_delete_messages=True,
                            can_restrict_members=True,
                            can_invite_users=True,
                            can_pin_messages=True,
                        ),
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
                    await message.edit(format_exc(e))
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


@Client.on_message(filters.command(["antich"], prefix))
async def anti_channels(client: Client, message: Message):
    if message.chat.type != "supergroup":
        await message.edit("<b>Not supported in non-supergroup chats</b>")
        return

    if len(message.command) == 1:
        if db.get("core.ats", f"antich{message.chat.id}", False):
            await message.edit(
                "<b>Blocking channels in this chat is enabled.\n"
                f"Disable with: </b><code>{prefix}antich disable</code>"
            )
        else:
            await message.edit(
                "<b>Blocking channels in this chat is disabled.\n"
                f"Enable with: </b><code>{prefix}antich enable</code>"
            )
    elif message.command[1] in ["enable", "on", "1", "yes", "true"]:
        db.set("core.ats", f"antich{message.chat.id}", True)
        group = await client.get_chat(message.chat.id)
        if group.linked_chat:
            db.set("core.ats", f"linked{message.chat.id}", group.linked_chat.id)
        else:
            db.set("core.ats", f"linked{message.chat.id}", 0)
        await message.edit("<b>Blocking channels in this chat enabled.</b>")
    elif message.command[1] in ["disable", "off", "0", "no", "false"]:
        db.set("core.ats", f"antich{message.chat.id}", False)
        await message.edit("<b>Blocking channels in this chat disabled.</b>")
    else:
        await message.edit(f"<b>Usage: {prefix}antich [enable|disable]</b>")

    update_cache()


@Client.on_message(filters.command(["delete_history", "dh"], prefix))
async def delete_history(client: Client, message: Message):
    cause = text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                user_for_delete, name = await get_user_and_name(message)
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(user_for_delete)
                await client.invoke(
                    functions.channels.DeleteParticipantHistory(
                        channel=channel, participant=user_id
                    )
                )

                await message.edit(
                    f"<code>History from <b>{name}</b> was deleted!</code>"
                    + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                await message.edit(format_exc(e))
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await check_username_or_id(cause.split(" ")[1]) == "channel":
                    user_to_delete = await client.get_chat(cause.split(" ")[1])
                elif await check_username_or_id(cause.split(" ")[1]) == "user":
                    user_to_delete = await client.get_users(cause.split(" ")[1])
                else:
                    await message.edit("<b>Invalid user type</b>")
                    return

                name = (
                    user_to_delete.first_name
                    if getattr(user_to_delete, "first_name", None)
                    else user_to_delete.title
                )

                try:
                    channel = await client.resolve_peer(message.chat.id)
                    user_id = await client.resolve_peer(user_to_delete.id)
                    await client.invoke(
                        functions.channels.DeleteParticipantHistory(
                            channel=channel, participant=user_id
                        )
                    )
                    await message.edit(
                        f"<code>History from </code><b>{name}</b><code> was deleted!</code>"
                        + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    await message.edit(format_exc(e))
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


@Client.on_message(filters.command(["report_spam", "rs"], prefix))
@with_reply
async def report_spam(client: Client, message: Message):
    try:
        channel = await client.resolve_peer(message.chat.id)

        user_id, name = await get_user_and_name(message)
        peer = await client.resolve_peer(user_id)
        await client.invoke(
            functions.channels.ReportSpam(
                channel=channel,
                participant=peer,
                id=[message.reply_to_message.id],
            )
        )
    except Exception as e:
        await message.edit(format_exc(e))
    else:
        await message.edit(f"<b>Message</a> from {name} was reported</b>")


@Client.on_message(filters.command("pin", prefix) & filters.me)
@with_reply
async def pin(_, message: Message):
    try:
        await message.reply_to_message.pin()
        await message.edit("<b>Pinned!</b>")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("unpin", prefix) & filters.me)
@with_reply
async def unpin(_, message: Message):
    try:
        await message.reply_to_message.unpin()
        await message.edit("<b>Unpinned!</b>")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("ro", prefix) & filters.me)
async def ro(client: Client, message: Message):
    if message.chat.type != "supergroup":
        await message.edit("<b>Invalid chat type</b>")
        return

    try:
        perms = message.chat.permissions
        perms_list = [
            perms.can_send_messages,
            perms.can_send_media_messages,
            perms.can_send_other_messages,
            perms.can_send_polls,
            perms.can_add_web_page_previews,
            perms.can_change_info,
            perms.can_invite_users,
            perms.can_pin_messages,
        ]
        db.set("core.ats", f"ro{message.chat.id}", perms_list)

        try:
            await client.set_chat_permissions(
                message.chat.id, ChatPermissions()
            )
        except (UserAdminInvalid, ChatAdminRequired):
            await message.edit("<b>No rights</b>")
        else:
            await message.edit(
                "<b>Read-only mode activated!\n"
                f"Turn off with:</b><code>{prefix}unro</code>"
            )
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("unro", prefix) & filters.me)
async def unro(client: Client, message: Message):
    if message.chat.type != "supergroup":
        await message.edit("<b>Invalid chat type</b>")
        return

    try:
        perms_list = db.get(
            "core.ats",
            f"ro{message.chat.id}",
            [True, True, True, False, False, False, False, False],
        )
        perms = ChatPermissions(
            can_send_messages=perms_list[0],
            can_send_media_messages=perms_list[1],
            can_send_other_messages=perms_list[2],
            can_send_polls=perms_list[3],
            can_add_web_page_previews=perms_list[4],
            can_change_info=perms_list[5],
            can_invite_users=perms_list[6],
            can_pin_messages=perms_list[7],
        )

        try:
            await client.set_chat_permissions(message.chat.id, perms)
        except (UserAdminInvalid, ChatAdminRequired):
            await message.edit("<b>No rights</b>")
        else:
            await message.edit("<b>Read-only mode disabled!</b>")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("antiraid", prefix) & filters.me)
async def antiraid(client: Client, message: Message):
    if message.chat.type != "supergroup":
        await message.edit("<b>Not supported in non-supergroup chats</b>")
        return

    if len(message.command) > 1 and message.command[1] == "on":
        db.set("core.ats", f"antiraid{message.chat.id}", True)
        group = await client.get_chat(message.chat.id)
        if group.linked_chat:
            db.set("core.ats", f"linked{message.chat.id}", group.linked_chat.id)
        else:
            db.set("core.ats", f"linked{message.chat.id}", 0)
        await message.edit(
            "<b>Anti-raid mode enabled!\n"
            f"Disable with: </b><code>{prefix}antiraid off</code>"
        )
    elif len(message.command) > 1 and message.command[1] == "off":
        db.set("core.ats", f"antiraid{message.chat.id}", False)
        await message.edit("<b>Anti-raid mode disabled</b>")
    else:
        # toggle
        if db.get("core.ats", f"antiraid{message.chat.id}", False):
            db.set("core.ats", f"antiraid{message.chat.id}", False)
            await message.edit("<b>Anti-raid mode disabled</b>")
        else:
            db.set("core.ats", f"antiraid{message.chat.id}", True)
            group = await client.get_chat(message.chat.id)
            if group.linked_chat:
                db.set(
                    "core.ats", f"linked{message.chat.id}", group.linked_chat.id
                )
            else:
                db.set("core.ats", f"linked{message.chat.id}", 0)
            await message.edit(
                "<b>Anti-raid mode enabled!\n"
                f"Disable with: </b><code>{prefix}antiraid off</code>"
            )

    update_cache()


@Client.on_message(filters.command(["welcome", "wc"], prefix) & filters.me)
async def welcome(_, message: Message):
    if message.chat.type != "supergroup":
        return await message.edit("<b>Unsupported chat type</b>")

    if len(message.command) > 1:
        text = message.text.split(maxsplit=1)[1]
        db.set("core.ats", f"welcome_enabled{message.chat.id}", True)
        db.set("core.ats", f"welcome_text{message.chat.id}", text)

        await message.edit(
            f"<b>Welcome enabled in this chat\nText:</b> <code>{text}</code>"
        )
    else:
        db.set("core.ats", f"welcome_enabled{message.chat.id}", False)
        await message.edit("<b>Welcome disabled in this chat</b>")

    update_cache()


modules_help["admintool"] = {
    "ban [reply]/[username/id]* [reason] [report_spam] [delete_history]": "ban user in chat",
    "unban [reply]/[username/id]* [reason]": "unban user in chat",
    "kick [reply]/[userid]* [reason] [report_spam] [delete_history]": "kick user out of chat",
    "mute [reply]/[userid]* [reason] [1m]/[1h]/[1d]/[1w]": "mute user in chat",
    "unmute [reply]/[userid]* [reason]": "unmute user in chat",
    "promote [reply]/[userid]* [prefix]": "promote user in chat",
    "demote [reply]/[userid]* [reason]": "demote user in chat",
    "tmute [reply]/[username/id]* [reason]": "delete all new messages from user in chat",
    "tunmute [reply]/[username/id]* [reason]": "stop deleting all messages from user in chat",
    "tmute_users": "list of tmuted (.tmute) users",
    "antich [enable/disable]": "turn on/off blocking channels in this chat",
    "delete_history [reply]/[username/id]* [reason]": "delete history from member in chat",
    "report_spam [reply]*": "report spam message in chat",
    "pin [reply]*": "Pin replied message",
    "unpin [reply]*": "Unpin replied message",
    "ro": "enable read-only mode",
    "unro": "disable read-only mode",
    "antiraid [on|off]": "when enabled, anyone who writes message will be blocked. Useful in raids. "
    "Running without arguments equals to toggling state",
    "welcome [text]*": "enable auto-welcome to new users in groups. "
    "Running without text equals to disable",
    "kickdel": "Kick all deleted accounts",
}
