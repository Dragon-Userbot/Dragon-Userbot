from pyrogram.types import Message
from pyrogram import filters
from utils import app


@app.on_message(filters.command('ws', ['.']) & filters.me)
def switch(client, message):
    text = ' '.join(message.command[1:])
    ru_keys = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё"№;%:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"""
    en_keys = """eicykengшщzh_fiwaproldgeiчsmit_bu.E"№;%:?ICYKENGШЩZH_FIWAPROLDGEIЧSMIT_BU,"""
    if text == '':
        if message.reply_to_message:
            reply_text = message.reply_to_message.text
            message.delete()
            change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
            reply_text = str.translate(reply_text, change)
            client.send_message(message.chat.id, reply_text)
        else:
            message.edit('No text for switch')
            time.sleep(3)
            message.delete()
    else:
        message.delete()
        change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
        text = str.translate(text, change)
        client.send_message(message.chat.id, text)
