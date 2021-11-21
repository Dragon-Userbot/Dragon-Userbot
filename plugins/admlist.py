from time import perf_counter
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from .utils.utils import modules_help, prefix
from .utils.db import db


@Client.on_message(filters.command("admlist", prefix) & filters.me)
async def ownlist(client: Client, message: Message):
    tstart = perf_counter()
    await message.edit("<code>Retrieving information... (it'll take some time)</code>")
    chatlist = []
    async for dialog in client.iter_dialogs():
        if dialog.chat.type in [ 'group', 'supergroup', 'channel']:
            try:
                _rself = await dialog.chat.get_member("me")
                if _rself.status in ["administrator", "creator"]:
                    if dialog.top_message is not None:
                        link = dialog.top_message.link
                    else:
                        link = 'null'
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

    for chat in chatlist:
        if chat['role'] == "creator" and chat['username'] is not None:
            owned_chats_with_username += f'<a href="{chat["link"]}">{chat["chat_name"]}</a> - @{chat["username"]}\n'
        elif chat['role'] == "creator":
            owned_chats += (
                f'<a href="{chat["link"]}">{chat["chat_name"]}</a>\n'
            )
        elif chat['role'] == "administrator":
            adminned_chats += (
                f'<a href="{chat["link"]}">{chat["chat_name"]}</a>\n'
            )
    tstop = perf_counter()
    await message.edit(
        adminned_chats + "\n" + owned_chats + "\n" + owned_chats_with_username + "\n\n" + f"Done at {int(tstop - tstart)} seconds."
    )


modules_help.update(
    {
        "admlist": """admlist - Get adminned and owned chats""",
        "admlist module": "Admlist: admlist",
    }
)
