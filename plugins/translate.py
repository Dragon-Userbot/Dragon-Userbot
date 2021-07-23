from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command('tr', prefix) & filters.me)
async def switch(client: Client, message: Message):
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
            await asyncio.sleep(3)
            await message.delete()
    else:
        change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
        text = str.translate(text, change)
        await message.edit(text)


modules_help.update({'translate': '''tr [text for translate] - message translator,
                                     tr - Reply to the message for translation''',
                     'translate module': 'Translate: tr'})
