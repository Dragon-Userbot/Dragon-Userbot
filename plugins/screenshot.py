from pyrogram import Client, filters
from pyrogram.raw import types, functions
from .utils.utils import modules_help

import time


@Client.on_message(filters.command('scr', ["."]) & filters.private & filters.me)
def screenshot(client, message):
    quantity = int(message.command[1])
    message.delete()
    for scr in range(quantity):
        time.sleep(0.1)
        client.send(functions.messages.SendScreenshotNotification(
            peer=client.resolve_peer(message.chat.id),
            reply_to_msg_id=0, random_id=client.rnd_id()))


modules_help.update({'screenshot': '''<b>Help for |screenshot|\nUsage:</b>
<code>.scr [amount of screenshot]</code>
<b>[Take a screenshot]
[This only works in private messages!]</b>''', 'screenshot module': '<b>• Screenshot</b>:<code> scr</code>\n'})
