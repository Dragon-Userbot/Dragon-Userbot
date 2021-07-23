from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from .utils.utils import modules_help, prefix
import asyncio


@Client.on_message(filters.command('type', prefix) & filters.me)
async def type(client: Client, message: Message):
    orig_text = ' '.join(message.command[1:])
    text = orig_text
    tbp = ""
    typing_symbol = "▒"

    while(tbp != orig_text):
        try:
            await message.edit(tbp + typing_symbol)
            await asyncio.sleep(0.1)

            tbp = tbp + text[0]
            text = text[1:]

            await message.edit(tbp)
            await asyncio.sleep(0.1)

        except FloodWait as e:
            time.sleep(e.x)


modules_help.update(
    {'type': '''type [What to print] - Typing emulation]\n[Don't use for a lot of characters. Your account may be banned!''',
     'type module': 'Type: type'})
