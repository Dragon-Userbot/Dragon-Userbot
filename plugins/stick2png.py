from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help
import os
import asyncio


@Client.on_message(filters.command(['stick2png', 'stp'], ['.']) & filters.me)
async def stick2png(client: Client, message: Message):
    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.sticker:
            if not reply.sticker.is_animated:
                await message.edit('<code>Picture processing...</code>')
                file = await client.download_media(message.reply_to_message, 'out.png')
                await client.send_photo(message.chat.id, 'downloads/out.png', reply_to_message_id=message.reply_to_message.message_id)
                await message.delete()
                os.remove('downloads/out.png')
            else:
                msg = await message.edit('<b>Stiker is animated!</b>')
                await asyncio.sleep(3)
                await msg.delete()    
        else:
            msg = await message.edit('<b>Reply to stiker!</b>')
            await asyncio.sleep(3)
            await msg.delete()


modules_help.update({'stick2png': '''<b>Help for |Stick to png|\nUsage:</b>
<code>.stp </code>
<b>[Reply to stiker]</b>''', 'stick2png module': '<b>• Stick2png</b>:<code> stick2png, stp</code>\n'})

