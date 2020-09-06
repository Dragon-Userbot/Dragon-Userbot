from pyrogram.types import Message
from pyrogram import Client, filters
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