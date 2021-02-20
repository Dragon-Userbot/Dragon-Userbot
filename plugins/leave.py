from pyrogram import Client, filters
from .utils.utils import modules_help
import asyncio


@Client.on_message(filters.command(['leave'], ['.']) & filters.me)
async def leave(client, message):
    m = await message.edit('<code>Goodbye...</code>')
    await asyncio.sleep(3)
    await client.leave_chat(chat_id=message.chat.id)
    

modules_help.update({'leave': '''<b>Help for |leave|\nUsage:</b>
<code>.leave</code>
<b>[Quit chat]</b>''', 'leave module': '<b>• Leave</b>:<code> leave</code>\n'})
