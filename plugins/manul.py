from pyrogram import Client, filters
from .utils.utils import modules_help
import time


@Client.on_message(filters.command('manul', ['.']) & filters.me)
async def manul(client, message):
    quantity = message.command[1]
    quantity = int(quantity) + 1
    print('manul')
    await message.delete()
    for i in range(1, quantity):
        await client.send_message(message.chat.id, f"{i} манула(ов)")
        time.sleep(0.2)


modules_help.update({'manul': '''<b>Help for |manul|\nUsage:</b>
<code>.manul [amount of manul]</code>
<b>[Release manuls]</b>''', 'manul module': '<b>• Manul</b>:<code> manul</code>\n'})
