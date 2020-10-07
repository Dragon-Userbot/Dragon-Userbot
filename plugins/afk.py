from pyrogram import Client, filters
from .utils.utils import modules_help

import datetime
import time


@Client.on_message(filters.command('afk', ['.']) & filters.me)
def afk(client, message):
    global start, end
    start = datetime.datetime.now().replace(microsecond=0)
    message.edit("<b>I'm going afk</b>")

    
@Client.on_message(filters.command('unafk', ['.']) & filters.me)
def unafk(client, message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = (end - start)
        message.edit(f"<b>I'm not AFK anymore.\nI was afk {afk_time}</b>")
        print(afk_time)
    except NameError:
        message.edit("<b>You weren't afk</b>")
        time.sleep(3)
        message.delete()


modules_help.update({'afk': '''<b>Help for |afk|\nUsage:</b>
<code>.afk</code>
<b>[To go to afk]</b>
<code>.unafk</code>
<b>[To get out of AFK]</b>''', 'afk module': '<b>• Afk</b>:<code> afk, unafk</code>\n'})
