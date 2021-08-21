from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
import os

date_dict = {}

@Client.on_message(filters.chat("@creationdatebot"), group=-1)
async def get_date(client: Client, message: Message):
    await client.read_history("@creationdatebot")
    date_dict.update({"date": message.text})


async def text(client: Client, message: Message):
    if message.text:
        return message.text
    else:
        return message.caption

async def chat_permissions(client: Client, message: Message):
    unmute_permissions = ChatPermissions(
        can_send_messages=message.chat.permissions.can_send_messages,
        can_send_media_messages=message.chat.permissions.can_send_media_messages,
        can_send_stickers=message.chat.permissions.can_send_stickers,
        can_send_animations=message.chat.permissions.can_send_animations,
        can_send_games=message.chat.permissions.can_send_games,
        can_use_inline_bots=message.chat.permissions.can_use_inline_bots,
        can_add_web_page_previews=message.chat.permissions.can_add_web_page_previews,
        can_send_polls=message.chat.permissions.can_send_polls,
        can_change_info=message.chat.permissions.can_change_info,
        can_invite_users=message.chat.permissions.can_invite_users,
        can_pin_messages=message.chat.permissions.can_pin_messages
    )
    return unmute_permissions


async def restart():
    await os.execvp("python3", ["python3", "main.py"])