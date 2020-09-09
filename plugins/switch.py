from pyrogram import Client, filters
from .utils.utils import modules_help

import time


@Client.on_message(filters.command('sw', ['.']) & filters.me)
def switch(client, message):
    text = ' '.join(message.command[1:])
    ru_keys = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё"№;%:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"""
    en_keys = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$%^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?"""
    if text == '':
        if message.reply_to_message:
            reply_text = message.reply_to_message.text
            change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
            reply_text = str.translate(reply_text, change)
            message.edit(reply_text)
        else:
            message.edit('No text for switch')
            time.sleep(3)
            message.delete()
    else:
        change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
        text = str.translate(text, change)
        message.edit(text)


modules_help.update({'switch': '''<b>Help for |switch|\nUsage:</b>
<code>.sw [text for switch]</code>
<b>[This is useful if you forgot to change the keyboard layout]</b>
<code>.sw </code>
<b>[Reply to the message to switch keyboard layout]</b>''', 'switch module': '<b>• Switch</b>:<code> sw</code>\n'})

