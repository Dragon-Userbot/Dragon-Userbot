# rewrote the module from @ Fl1yd
from pyrogram.types import Message
from pyrogram import Client, filters
from .utils.utils import modules_help

import requests


@Client.on_message(filters.command('weather', ['.']) & filters.me)
async def weather(client: Client, message: Message):
    city = message.command[1]
    await message.edit("```Processing the request...```")
    r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
    await message.edit(f"```City: {r.text}```")
    await client.send_document(chat_id=message.chat.id, document=f'http://wttr.in/{city}_2&lang=en.png', reply_to_message_id=message.message_id)


modules_help.update({'weather': '''weather [city] - Get the weather in the selected city''',
                     'weather module': 'Weather: weather'})
