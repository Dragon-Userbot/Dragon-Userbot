from pyrogram import Message, Filters
from utils import app



@app.on_message(Filters.command('sw', ['.']) & Filters.me)
def switch(client, message):
    text = ' '.join(message.command[1:])
    ru_keys = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё"№;%:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"""
    en_keys = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$%^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?"""
    if message.reply_to_message:
        reply_text = message.reply_to_message.text
        message.delete()
        change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
        reply_text = str.translate(reply_text, change)
        client.send_message(message.chat.id, reply_text)
    else:
        message.delete()
        change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
        text = str.translate(text, change)
        client.send_message(message.chat.id, text)