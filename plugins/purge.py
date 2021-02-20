from pyrogram import Client, filters
from .utils.utils import modules_help

import asyncio


@Client.on_message(filters.command('del', ["."]) & filters.me)
async def del_msg(client, message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        await message.delete()
        await client.delete_messages(message.chat.id, message_id)


@Client.on_message(filters.command('purge', ["."]) & filters.me)
async def purge(client, message):
    if message.reply_to_message:
        start_message = message.reply_to_message.message_id
        end_message = message.message_id
        message_ids = range(start_message, end_message)
        messages = await client.get_messages(chat_id=message.chat.id, message_ids=message_ids, replies=0)
        messages_list = []
        quantity = 0
        for message_iter in messages:
            if len(messages_list) == 100:
                await client.delete_messages(chat_id=message.chat.id, message_ids=message_ids)
            else:
                messages_list.append(message_iter.message_id)

        if messages_list:
            await client.delete_messages(chat_id=message.chat.id,message_ids=messages_list)

        await message.edit('<b>Сleaning was successful!</b>')
        await asyncio.sleep(3)
        await message.delete()
    else:
        await message.edit('<b>Reply to a message after which you want to delete messages</b>')


modules_help.update({'purge': '''<b>Help for |purge|\nUsage:</b>
<code>.purge</code>
<b>[Reply to a message after which you want to delete messages]
<code>.del</code>
[Reply to the message you want to delete]</b>''', 'purge module': '<b>• Purge</b>:<code> purge, del</code>\n'})