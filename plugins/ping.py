from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from time import perf_counter


@Client.on_message(filters.command(['ping', 'p'], prefix) & filters.me)
async def ping(client: Client, message: Message):
    start = perf_counter()
    await message.edit('Pong')
    end = perf_counter()
    ping = end - start
    await message.edit(f'<b>Ping</b><code> {round(ping, 3)}s</code>')


modules_help.update({'ping': '''ping - To find out the ping''', 'ping module': 'Ping: ping\n'})
