from pyrogram import Client, filters
from .utils.utils import modules_help
import time

@Client.on_message(filters.command(['leave'], ['.']) & filters.me)
def leave(client, message):
    m = message.edit('<code>Goodbye...</code>')
    time.sleep(3)
    client.leave_chat(chat_id=message.chat.id)


modules_help.update({'leave': '''<b>Help for |leave|\nUsage:</b>
<code>.leave</code>
<b>[Quit chat]</b>''', 'leave module': '<b>• Leave</b>:<code> leave</code>\n'})
