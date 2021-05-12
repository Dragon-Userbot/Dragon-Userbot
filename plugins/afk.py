from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help


import datetime
import asyncio


@Client.on_message(filters.command('afk', ['.']) & filters.me)
async def afk(client: Client, message: Message):
    global start, end
    start = datetime.datetime.now().replace(microsecond=0)
    await message.edit("<b>I'm going afk</b>")

@Client.on_message(filters.command('unafk', ['.']) & filters.me)
async def unafk(client: Client, message: Message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = (end - start)
        await message.edit(f"<b>I'm not AFK anymore.\nI was afk {afk_time}</b>")
        print(afk_time)
    except NameError:
        await message.edit("<b>You weren't afk</b>")
        await asyncio.sleep(3)
        await message.delete()


modules_help.update({'afk': '''<b>Help for |afk|\nUsage:</b>
<code>.afk</code>
<b>[To go to afk]</b>
<code>.unafk</code>
<b>[To get out of AFK]</b>''', 'afk module': '<b>• Afk</b>:<code> afk, unafk</code>\n'})
