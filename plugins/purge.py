from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix

import asyncio


@Client.on_message(filters.command("del", prefix) & filters.me)
async def del_msg(client: Client, message: Message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        await message.delete()
        await client.delete_messages(message.chat.id, message_id)


@Client.on_message(filters.command("purge", prefix) & filters.me)
async def purge(client: Client, message: Message):
    messages_to_purge = []
    if message.reply_to_message:
        async for msg in client.iter_history(
            chat_id=message.chat.id,
            offset_id=message.reply_to_message.message_id,
            reverse=True,
        ):
            messages_to_purge.append(msg)
    not_deleted_messages = []
    for msg in messages_to_purge:
        try:
            res = await msg.delete()
            if not res:
                not_deleted_messages.append(msg)
        except:
            not_deleted_messages.append(msg)
    if len(not_deleted_messages) > 0:
        links = "\n".join([msg.link for msg in not_deleted_messages])
        msg = await client.send_message(
            message.chat.id,
            f"<b>I can't delete some messages :(</b>\nLinks:<br>{links}",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    else:
        await asyncio.sleep(1)
        msg = await client.send_message(
            message.chat.id, f"<b>Сleaning was successful!</b>", parse_mode="HTML"
        )
        await asyncio.sleep(1.20)
        await msg.delete()


modules_help.update(
    {
        "purge": """purge - Reply to a message after which you want to delete messages, del - Reply to the message you want to delete""",
        "purge module": "Purge: purge, del",
    }
)
