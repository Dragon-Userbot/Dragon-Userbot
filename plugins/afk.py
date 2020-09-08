from pyrogram import Client, filters

import datetime
import time


@Client.on_message(filters.command('afk', ['.']) & filters.me)
def afk(client, message):
    global start, end
    start = datetime.datetime.now().replace(microsecond=0)
    message.edit("<b>I'm going afk</b>")

    @Client.on_message(filters.text)
    def my_handler(client, message):
        try:
            if f'@{client.get_me().username}' in message.text: 
                end = datetime.datetime.now().replace(microsecond=0)
                afk_time = (end - start)
                client.send_message(message.chat.id, f"<b>I'm afk now.\n[ {afk_time} ]</b>")
                print(afk_time)

        except NameError:
            pass



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
