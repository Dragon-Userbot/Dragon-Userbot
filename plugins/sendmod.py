from pyrogram import Client, filters
from pyrogram.raw import types, functions
from .utils.utils import modules_help

import asyncio

@Client.on_message(filters.command(['sendmod', 'sm'], ["."]) & filters.me)
async def sendmod(client, message):
    mod_name = message.command[1]
    try:
        await message.edit('<code>Dispatch...</code>')
        await client.send_document(message.chat.id, f"plugins/{mod_name.lower()}.py", caption=modules_help[mod_name.lower()])
        await message.delete()
    except:
        await message.edit('<b>Invalid module name!</b>')
        await asyncio.sleep(5)
        await message.delete()


modules_help.update({'sendmod': '''<b>Help for |sendmod|\nUsage:</b>
<code>.sendmod |module name|</code>
<b>[Send one of the modules to the interlocutor]</b>''', 'sendmod module': '<b>• Sendmod</b>:<code> sendmod</code>\n'})
