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

import json
from html import escape as t
from time import perf_counter
from typing import AsyncGenerator, Optional, List, Union

from pyrogram import Client, filters
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram import types, raw, utils, enums
from pyrogram.types.object import Object

from utils.misc import modules_help, prefix
from utils.scripts import format_exc


class Chat(Object):
    def __init__(
        self,
        *,
        client: "Client" = None,
        id: int,
        type: "enums.ChatType",
        is_verified: bool = None,
        is_restricted: bool = None,
        is_creator: bool = None,
        is_scam: bool = None,
        is_fake: bool = None,
        is_support: bool = None,
        title: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        photo: "types.ChatPhoto" = None,
        bio: str = None,
        description: str = None,
        dc_id: int = None,
        has_protected_content: bool = None,
        invite_link: str = None,
        pinned_message=None,
        sticker_set_name: str = None,
        can_set_sticker_set: bool = None,
        members_count: int = None,
        restrictions: List["types.Restriction"] = None,
        permissions: "types.ChatPermissions" = None,
        distance: int = None,
        linked_chat: "types.Chat" = None,
        send_as_chat: "types.Chat" = None,
        available_reactions: Optional["types.ChatReactions"] = None,
        is_admin: bool = False,
        deactivated: bool = False,
    ):
        super().__init__(client)

        self.id = id
        self.type = type
        self.is_verified = is_verified
        self.is_restricted = is_restricted
        self.is_creator = is_creator
        self.is_scam = is_scam
        self.is_fake = is_fake
        self.is_support = is_support
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.bio = bio
        self.description = description
        self.dc_id = dc_id
        self.has_protected_content = has_protected_content
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.members_count = members_count
        self.restrictions = restrictions
        self.permissions = permissions
        self.distance = distance
        self.linked_chat = linked_chat
        self.send_as_chat = send_as_chat
        self.available_reactions = available_reactions
        self.is_admin = is_admin
        self.deactivated = deactivated

    @staticmethod
    def _parse_user_chat(client, user: raw.types.User) -> "Chat":
        peer_id = user.id

        return Chat(
            id=peer_id,
            type=enums.ChatType.BOT if user.bot else enums.ChatType.PRIVATE,
            is_verified=getattr(user, "verified", None),
            is_restricted=getattr(user, "restricted", None),
            is_scam=getattr(user, "scam", None),
            is_fake=getattr(user, "fake", None),
            is_support=getattr(user, "support", None),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo=types.ChatPhoto._parse(
                client, user.photo, peer_id, user.access_hash
            ),
            restrictions=types.List(
                [types.Restriction._parse(r) for r in user.restriction_reason]
            )
            or None,
            dc_id=getattr(getattr(user, "photo", None), "dc_id", None),
            client=client,
        )

    @staticmethod
    def _parse_chat_chat(client, chat: raw.types.Chat) -> "Chat":
        peer_id = -chat.id
        return Chat(
            id=peer_id,
            type=enums.ChatType.GROUP,
            title=chat.title,
            is_creator=getattr(chat, "creator", None),
            photo=types.ChatPhoto._parse(
                client, getattr(chat, "photo", None), peer_id, 0
            ),
            permissions=types.ChatPermissions._parse(
                getattr(chat, "default_banned_rights", None)
            ),
            members_count=getattr(chat, "participants_count", None),
            dc_id=getattr(getattr(chat, "photo", None), "dc_id", None),
            has_protected_content=getattr(chat, "noforwards", None),
            client=client,
            is_admin=True if getattr(chat, "admin_rights", False) else False,
            deactivated=getattr(chat, "deactivated"),
        )

    @staticmethod
    def _parse_channel_chat(client, channel: raw.types.Channel) -> "Chat":
        peer_id = utils.get_channel_id(channel.id)
        restriction_reason = getattr(channel, "restriction_reason", [])

        return Chat(
            id=peer_id,
            type=enums.ChatType.SUPERGROUP
            if getattr(channel, "megagroup", None)
            else enums.ChatType.CHANNEL,
            is_verified=getattr(channel, "verified", None),
            is_restricted=getattr(channel, "restricted", None),
            is_creator=getattr(channel, "creator", None),
            is_scam=getattr(channel, "scam", None),
            is_fake=getattr(channel, "fake", None),
            title=channel.title,
            username=getattr(channel, "username", None),
            photo=types.ChatPhoto._parse(
                client,
                getattr(channel, "photo", None),
                peer_id,
                getattr(channel, "access_hash", 0),
            ),
            restrictions=types.List(
                [types.Restriction._parse(r) for r in restriction_reason]
            )
            or None,
            permissions=types.ChatPermissions._parse(
                getattr(channel, "default_banned_rights", None)
            ),
            members_count=getattr(channel, "participants_count", None),
            dc_id=getattr(getattr(channel, "photo", None), "dc_id", None),
            has_protected_content=getattr(channel, "noforwards", None),
            is_admin=True if getattr(channel, "admin_rights", False) else False,
            client=client,
        )

    @staticmethod
    def _parse(
        client,
        message: Union[raw.types.Message, raw.types.MessageService],
        users: dict,
        chats: dict,
        is_chat: bool,
    ) -> "Chat":
        from_id = utils.get_raw_peer_id(message.from_id)
        peer_id = utils.get_raw_peer_id(message.peer_id)
        chat_id = (peer_id or from_id) if is_chat else (from_id or peer_id)

        if isinstance(message.peer_id, raw.types.PeerUser):
            return Chat._parse_user_chat(client, users[chat_id])

        if isinstance(message.peer_id, raw.types.PeerChat):
            return Chat._parse_chat_chat(client, chats[chat_id])

        return Chat._parse_channel_chat(client, chats[chat_id])

    @staticmethod
    def _parse_dialog(client, peer, users: dict, chats: dict):
        if isinstance(peer, raw.types.PeerUser):
            return Chat._parse_user_chat(client, users[peer.user_id])
        elif isinstance(peer, raw.types.PeerChat):
            return Chat._parse_chat_chat(client, chats[peer.chat_id])
        else:
            return Chat._parse_channel_chat(client, chats[peer.channel_id])


class Dialog(Object):
    def __init__(
        self,
        *,
        client: "Client" = None,
        chat: "types.Chat",
        top_message: "types.Message",
        unread_messages_count: int,
        unread_mentions_count: int,
        unread_mark: bool,
        is_pinned: bool,
    ):
        super().__init__(client)

        self.chat = chat
        self.top_message = top_message
        self.unread_messages_count = unread_messages_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_mark = unread_mark
        self.is_pinned = is_pinned

    @staticmethod
    def _parse(
        client, dialog: "raw.types.Dialog", messages, users, chats
    ) -> "Dialog":
        return Dialog(
            chat=Chat._parse_dialog(client, dialog.peer, users, chats),
            top_message=messages.get(utils.get_peer_id(dialog.peer)),
            unread_messages_count=dialog.unread_count,
            unread_mentions_count=dialog.unread_mentions_count,
            unread_mark=dialog.unread_mark,
            is_pinned=dialog.pinned,
            client=client,
        )


async def get_dialogs(
    self: "Client", limit: int = 0
) -> Optional[AsyncGenerator["types.Dialog", None]]:
    current = 0
    total = limit or (1 << 31) - 1
    limit = min(100, total)
    offset_date = 0
    offset_id = 0
    offset_peer = raw.types.InputPeerEmpty()
    while True:
        r = await self.invoke(
            raw.functions.messages.GetDialogs(
                offset_date=offset_date,
                offset_id=offset_id,
                offset_peer=offset_peer,
                limit=limit,
                hash=0,
            ),
            sleep_threshold=60,
        )
        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        messages = {}
        for message in r.messages:
            if isinstance(message, raw.types.MessageEmpty):
                continue
            chat_id = utils.get_peer_id(message.peer_id)
            messages[chat_id] = await types.Message._parse(
                self, message, users, chats
            )
        dialogs = []
        for dialog in r.dialogs:
            if not isinstance(dialog, raw.types.Dialog):
                continue
            dialogs.append(Dialog._parse(self, dialog, messages, users, chats))
        if not dialogs:
            return
        last = dialogs[-1]
        offset_id = last.top_message.id
        offset_date = utils.datetime_to_timestamp(last.top_message.date)
        offset_peer = await self.resolve_peer(last.chat.id)
        for dialog in dialogs:
            yield dialog
            current += 1
            if current >= total:
                return


@Client.on_message(filters.command("admlist", prefix) & filters.me)
async def admlist(client: Client, message: types.Message):
    await message.edit(
        "<b>Retrieving information... (it'll take some time)</b>"
    )

    start = perf_counter()
    try:
        adminned_chats = []
        owned_chats = []
        owned_usernamed_chats = []
        async for dialog in get_dialogs(client):
            chat = dialog.chat
            if getattr(chat, "deactivated", False):
                continue
            if getattr(chat, "is_creator", False) and getattr(
                chat, "username", None
            ):
                owned_usernamed_chats.append(chat)
            elif getattr(chat, "is_creator", False):
                owned_chats.append(chat)
            elif getattr(chat, "is_admin", False):
                adminned_chats.append(chat)

        text = "<b>Adminned chats:</b>\n"
        for index, chat in enumerate(adminned_chats):
            cid = str(chat.id).replace("-100", "")
            text += f"{index + 1}. <a href=https://t.me/c/{cid}/1>{chat.title}</a>\n"

        text += "\n<b>Owned chats:</b>\n"
        for index, chat in enumerate(owned_chats):
            cid = str(chat.id).replace("-100", "")
            text += f"{index + 1}. <a href=https://t.me/c/{cid}/1>{chat.title}</a>\n"

        text += "\n<b>Owned chats with username:</b>\n"
        for index, chat in enumerate(owned_usernamed_chats):
            cid = str(chat.id).replace("-100", "")
            text += (
                f"{index + 1}. <a href=https://t.me/{cid}>{chat.title}</a>\n"
            )

        stop = perf_counter()
        total_count = (
            len(adminned_chats) + len(owned_chats) + len(owned_usernamed_chats)
        )
        await message.edit(
            text + "\n"
            f"<b><u>Total:</u></b> {total_count}"
            f"\n<b><u>Adminned chats:</u></b> {len(adminned_chats)}\n"
            f"<b><u>Owned chats:</u></b> {len(owned_chats)}\n"
            f"<b><u>Owned chats with username:</u></b> {len(owned_usernamed_chats)}\n\n"
            f"Done at {round(stop - start, 3)} seconds."
        )
    except Exception as e:
        await message.edit(format_exc(e))
        return


@Client.on_message(filters.command("admcount", prefix) & filters.me)
async def admcount(client: Client, message: types.Message):
    await message.edit(
        "<b>Retrieving information... (it'll take some time)</b>"
    )

    start = perf_counter()
    try:
        adminned_chats = 0
        owned_chats = 0
        owned_usernamed_chats = 0
        async for dialog in get_dialogs(client):
            chat = dialog.chat
            if getattr(chat, "deactivated", False):
                continue
            if getattr(chat, "is_creator", False) and getattr(
                chat, "username", None
            ):
                owned_usernamed_chats += 1
            elif getattr(chat, "is_creator", False):
                owned_chats += 1
            elif getattr(chat, "is_admin", False):
                adminned_chats += 1

        stop = perf_counter()
        total_count = adminned_chats + owned_chats + owned_usernamed_chats
        await message.edit(
            f"<b><u>Total:</u></b> {adminned_chats + owned_chats + owned_usernamed_chats}"
            f"\n<b><u>Adminned chats:</u></b> {adminned_chats}\n"
            f"<b><u>Owned chats:</u></b> {owned_chats}\n"
            f"<b><u>Owned chats with username:</u></b> {owned_usernamed_chats}\n\n"
            f"Done at {round(stop - start, 3)} seconds.\n\n"
            f"<b>Get full list: </b><code>{prefix}admlist</code>"
        )
    except Exception as e:
        await message.edit(format_exc(e))
        return


modules_help["admlist"] = {
    "admcount": "Get count of adminned and owned chats",
    "admlist": "Get list of adminned and owned chats",
}
