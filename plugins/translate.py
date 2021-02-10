from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('tr', ['.']) & filters.me)
async def switch(client, message):
    text = ' '.join(message.command[1:])
    ru_keys = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё"№;%:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"""
    en_keys = """eicykengшщzh_fiwaproldgeiчsmit_bu.E"№;%:?ICYKENGШЩZH_FIWAPROLDGEIЧSMIT_BU,"""
    if text == '':
        if message.reply_to_message:
            reply_text = message.reply_to_message.text
            change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
            reply_text = str.translate(reply_text, change)
            await message.edit(reply_text)
        else:
            await message.edit('No text for switch')
            time.sleep(3)
            await message.delete()
    else:
        change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
        text = str.translate(text, change)
        await message.edit(text)


modules_help.update({'translate': '''<b>Help for |translate|\nUsage:</b>
<code>.tr [text for translate]</code>
<b>[message translator]</b>
<code>.tr </code>
<b>[Reply to the message for translation]</b>''', 'translate module': '<b>• Translate</b>:<code> tr</code>\n'})
