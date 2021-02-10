from pyrogram import Client, filters
from .utils.utils import modules_help

import time


@Client.on_message(filters.command('statspam', ['.']) & filters.me)
async def statspam(client, message):
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        time.sleep(0.1)
        await msg.delete()
        time.sleep(0.1)

@Client.on_message(filters.command('spam', ['.']) & filters.me)
async def spam(client, message):
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        time.sleep(0.15)
        

modules_help.update({'spam': '''<b>Help for |spam|\nUsage:</b>
<code>.spam [amount of spam] [spam text]</code>
<b>[Start spam]</b>
<code>.statspam [amount of spam] [spam text]</code>
<b>[Send and delete]</b>''', 'spam module': '<b>• Spam</b>:<code> spam, statspam</code>\n'})
