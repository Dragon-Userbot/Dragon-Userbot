from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw import types, functions
from .utils.utils import modules_help

import asyncio


@Client.on_message(filters.command(['scr', 'screenshot'], ["."]) & filters.private & filters.me)
async def screenshot(client: Client, message: Message):
    quantity = int(message.command[1])
    await message.delete()
    for scr in range(quantity):
        await asyncio.sleep(0.1)
        await client.send(functions.messages.SendScreenshotNotification(
            peer= await client.resolve_peer(message.chat.id),
            reply_to_msg_id=0, random_id=client.rnd_id()))


modules_help.update({'screenshot': '''<b>Help for |screenshot|\nUsage:</b>
<code>.scr [amount of screenshot]</code>
<b>[Take a screenshot]</b>
<b>[This only works in private messages!]</b>''', 'screenshot module': '<b>• Screenshot</b>:<code> scr</code>\n'})
