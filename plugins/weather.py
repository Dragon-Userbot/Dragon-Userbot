#rewrote the module from @ Fl1yd

from pyrogram import Client, filters
from .utils.utils import modules_help

import requests


@Client.on_message(filters.command('weather', ['.']) & filters.me)
async def weather(client, message):
    city = message.command[1]
    await message.edit("<code>Processing the request...</code>")
    r = requests.get(f"https://wttr.in/{city}?0?q?T&lang=en")
    await message.edit(f"```City: {r.text}```")

    
modules_help.update({'weather': '''<b>Help for |weather|\nUsage:</b>
<code>.weather [city]</code>
<b>[Get the weather in the selected city]</b>''', 'weather module': '<b>• Weather</b>:<code> weather</code>\n'})

