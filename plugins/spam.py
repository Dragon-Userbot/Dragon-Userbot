from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help

import asyncio


@Client.on_message(filters.command('statspam', ['.']) & filters.me)
async def statspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.1)
        await msg.delete()
        await asyncio.sleep(0.1)

@Client.on_message(filters.command('spam', ['.']) & filters.me)
async def spam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.15)
        
@Client.on_message(filters.command('fastspam', ['.']) & filters.me)
async def fastspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.02)

@Client.on_message(filters.command('slowspam', ['.']) & filters.me)
async def slowspam(client: Client, message: Message):
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    await message.delete()
    for i in range(quantity):
        msg = await client.send_message(message.chat.id, spam_text)
        await asyncio.sleep(0.9)


modules_help.update({'spam': '''<b>Help for |spam|\nUsage:</b>
<code>.spam [amount of spam] [spam text]</code>
<b>[Start spam]</b>
<code>.statspam [amount of spam] [spam text]</code>
<b>[Send and delete]</b>
<code>.fastspam [amount of spam] [spam text]</code>
<b>[Start fast spam]</b>
<code>.slowspam [amount of spam] [spam text]</code>
<b>[Start slow spam]</b>''', 'spam module': '<b>• Spam</b>:<code> spam, statspam, slowspam, fastspam</code>\n'})
