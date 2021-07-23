from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
import asyncio


@Client.on_message(filters.command(['leave_chat'], prefix) & filters.me)
async def leave_chat(client: Client, message: Message):
    m = await message.edit('<code>Goodbye...</code>')
    await asyncio.sleep(3)
    await client.leave_chat(chat_id=message.chat.id)
    

modules_help.update({'leave_chat': '''leave_chat - Quit chat''', 'leave_chat module': 'Leave_chat: leave_chat'})
