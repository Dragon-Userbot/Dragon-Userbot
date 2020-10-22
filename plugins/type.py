from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from .utils.utils import modules_help
import time


@Client.on_message(filters.command('type', ['.']) & filters.me)
def type(client, message):
    orig_text =  ' '.join(message.command[1:])
    text = orig_text
    tbp = "" 
    typing_symbol = "▒"
 
    while(tbp != orig_text):
        try:
            message.edit(tbp + typing_symbol)
            time.sleep(0.1)
 
            tbp = tbp + text[0]
            text = text[1:]
 
            message.edit(tbp)
            time.sleep(0.1)

        except FloodWait as e:
            time.sleep(e.x)


modules_help.update({'type': '''<b>Help for |Type|\nUsage:</b>
[Do not use for a large number of characters, it can be banned!]
<code>.type [What to print]</code>
<b>[Typing emulation]</b>''', 'type module': '<b>• Type</b>:<code> type</code>\n'})
