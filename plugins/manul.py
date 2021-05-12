from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help
import asyncio


@Client.on_message(filters.command('manul', ['.']) & filters.me)
async def manul(client: Client, message: Message):
    quantity = message.command[1]
    quantity = int(quantity) + 1
    print('manul')
    await message.delete()
    for i in range(1, quantity):
        await client.send_message(message.chat.id, f"{i} манула(ов)")
        await asyncio.sleep(0.2)


modules_help.update({'manul': '''<b>Help for |manul|\nUsage:</b>
<code>.manul [amount of manul]</code>
<b>[Release manuls]</b>''', 'manul module': '<b>• Manul</b>:<code> manul</code>\n'})
