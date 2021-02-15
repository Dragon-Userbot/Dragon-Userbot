from pyrogram import Client, filters
from .utils.utils import modules_help
from time import perf_counter


@Client.on_message(filters.command(['ping', 'p'], ['.']) & filters.me)
async def ping(client, message):
    start = perf_counter()
    await message.edit('Pong')
    end = perf_counter()
    ping = end - start
    await message.edit(f'<b>Ping</b><code> {round(ping, 3)}s</code>')


modules_help.update({'ping': '''<b>Help for |ping|\nUsage:</b>
<code>.ping</code>
<b>[To find out the ping]</b>''', 'ping module': '<b>• Ping</b>:<code> ping</code>\n'})
