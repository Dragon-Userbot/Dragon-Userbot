from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('pin', ['.']) & filters.me)
def pin(client, message):
    try:
        message_id = message.reply_to_message.message_id
        client.pin_chat_message(message.chat.id, message_id)
        message.edit('<code>Pinned successfully! </code>')
    except:
        message.edit('<b>[Reply to the message you want to pin]\n[Does not work in private messages!]</b>')


modules_help.update({'pin': '''<b>Help for |pin|\nUsage:</b>
<code>.pin</code>
<b>[Pin any message]
[Reply to the message you want to pin]
[Does not work in private messages!]</b>''', 'pin module': '<b>• Pin</b>:<code> pin</code>\n'})
