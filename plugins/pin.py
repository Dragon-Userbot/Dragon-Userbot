from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help


@Client.on_message(filters.command('pin', ['.']) & filters.me)
async def pin(client: Client, message: Message):
    try:
        message_id = message.reply_to_message.message_id
        await client.pin_chat_message(message.chat.id, message_id)
        await message.edit('<code>Pinned successfully! </code>')
    except:
        await message.edit('<b>[Reply to the message you want to pin]\n[Does not work in private messages!]</b>')


modules_help.update({'pin': '''<b>Help for |pin|\nUsage:</b>
<code>.pin</code>
<b>[Pin any message]
[Reply to the message you want to pin]</b>''', 'pin module': '<b>• Pin</b>:<code> pin</code>\n'})
