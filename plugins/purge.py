from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix

import asyncio


@Client.on_message(filters.command('del', prefix) & filters.me)
async def del_msg(client: Client, message: Message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        await message.delete()
        await client.delete_messages(message.chat.id, message_id)


@Client.on_message(filters.command('purge', prefix) & filters.me)
async def purge(client: Client, message: Message):
    if message.reply_to_message:
        await message.delete()
        message_ids = []
        for a_s_message_id in range(message.reply_to_message.message_id, message.message_id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
                )
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )
    await asyncio.sleep(1)
    msg = await client.send_message(
        message.chat.id,
        f"<b>Сleaning was successful!</b>",
        parse_mode='HTML')
    await asyncio.sleep(1.20)
    await msg.delete()


modules_help.update({'purge': '''purge - Reply to a message after which you want to delete messages, del - Reply to the message you want to delete''',
                     'purge module': 'Purge: purge, del'})
