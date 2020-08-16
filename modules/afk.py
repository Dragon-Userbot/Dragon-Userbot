from pyrogram import Message, Filters
from utils import app

import datetime
import time


@app.on_message(Filters.command('afk', ['.']) & Filters.me)
def afk(client, message):
    global start, end
    start = datetime.datetime.now().replace(microsecond=0)
    message.edit("<b>I'm going afk</b>")


@app.on_message(Filters.command('unafk', ['.']) & Filters.me)
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