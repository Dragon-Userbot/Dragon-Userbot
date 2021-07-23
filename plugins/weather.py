# rewrote the module from @ Fl1yd
from pyrogram.types import Message
from pyrogram import Client, filters
from .utils.utils import modules_help, prefix

import requests
import os


def get_pic(city):
    file_name = f'{city}.png'
    with open(file_name, 'wb') as pic:
        response = requests.get('http://wttr.in/{citys}_2&lang=en.png', stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            pic.write(block)
        return file_name

@Client.on_message(filters.command('weather', prefix) & filters.me)
async def weather(client: Client, message: Message):
    city = message.command[1]
    await message.edit("```Processing the request...```")
    r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
    await message.edit(f"```City: {r.text}```")
    await client.send_document(chat_id=message.chat.id, document=get_pic(city), reply_to_message_id=message.message_id)
    os.remove(f'{city}.png')


modules_help.update({'weather': '''weather [city] - Get the weather in the selected city''',
                     'weather module': 'Weather: weather'})
