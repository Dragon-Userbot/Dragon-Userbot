from time import perf_counter
from pyrogram import Client, filters
from pyrogram.types import Message
from html import escape as t
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from .utils.utils import modules_help, prefix
from .utils.db import db


@Client.on_message(filters.command("admlist", prefix) & filters.me)
async def ownlist(client: Client, message: Message):
    tstart = perf_counter()
    await message.edit("<code>Retrieving information... (it'll take some time)</code>")
    chatlist = []
    async for dialog in client.iter_dialogs():
        if dialog.chat.type in ["group", "supergroup", "channel"]:
            try:
                _rself = await dialog.chat.get_member("me")
                if _rself.status in ["administrator", "creator"]:
                    if dialog.top_message is not None:
                        link = dialog.top_message.link
                    else:
                        link = "null"
                    chatlist.append(
                        {
                            "chat_name": dialog.chat.title,
                            "chat_id": dialog.chat.id,
                            "role": _rself.status,
                            "username": dialog.chat.username,
                            "link": link,
                        }
                    )
            except UserNotParticipant:
                pass

    adminned_chats = "<b>Adminned chats:</b>\n"
    owned_chats = "<b>Owned chats:</b>\n"
    owned_chats_with_username = "<b>Owned chats with username:</b>\n"

    c_adminned_chats = 0
    c_owned_chats = 0
    c_owned_chats_with_username = 0

    for chat in chatlist:
        if chat["role"] == "creator" and chat["username"] is not None:
            c_owned_chats_with_username += 1
            owned_chats_with_username += f'{c_owned_chats_with_username}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a> - @{chat["username"]}\n'
        elif chat["role"] == "creator":
            c_owned_chats += 1
            owned_chats += f'{c_owned_chats}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a>\n'
        elif chat["role"] == "administrator":
            c_adminned_chats += 1
            adminned_chats += f'{c_adminned_chats}. <a href="{chat["link"]}">{t(chat["chat_name"])}</a>\n'
    stats = f"<b><u>Total:</u></b> {len(chatlist)}\n<b><u>Adminned chats:</u></b> {c_adminned_chats}\n<b><u>Owned chats:</u></b> {c_owned_chats}\n<b><u>Owned chats with username:</u></b> {c_owned_chats_with_username}"
    tstop = perf_counter()
    await message.edit(
        adminned_chats
        + "\n"
        + owned_chats
        + "\n"
        + owned_chats_with_username
        + "\n"
        + stats
        + "\n\n"
        + f"Done at {int(tstop - tstart)} seconds.",
        disable_web_page_preview=True,
    )


modules_help.update(
    {
        "admlist": """admlist - Get adminned and owned chats""",
        "admlist module": "Admlist: admlist",
    }
)
