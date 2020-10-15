from pyrogram import Client, filters
from .utils.utils import modules_help

import time


@Client.on_message(filters.command('spam', ['.']) & filters.me)
def spam(client, message):
    quantity = message.command[1]
    spam_text = ' '.join(message.command[2:])
    quantity = int(quantity)
    message.delete()
    for i in range(quantity):
        client.send_message(message.chat.id, spam_text)
        time.sleep(0.2)


modules_help.update({'spam': '''<b>Help for |spam|\nUsage:</b>
<code>.spam [amount of spam] [spam text]</code>
<b>[Start spam]</b>''', 'spam module': '<b>• Spam</b>:<code> spam</code>\n'})
