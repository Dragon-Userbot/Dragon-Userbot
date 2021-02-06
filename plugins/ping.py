from pyrogram import Client, filters
from .utils.utils import modules_help
from time import perf_counter


@Client.on_message(filters.command('ping', ['.']) & filters.me)
def ping(client, message):
    start = datetime.datetime.now()
    message.edit('Pong')
    end = datetime.datetime.now()
    ping = (end - start).microseconds / 1000
    message.edit('Ping\n<code>{}</code>'.format(ping))


modules_help.update({'ping': '''<b>Help for |ping|\nUsage:</b>
<code>.ping</code>
<b>[To find out the ping]</b>''', 'ping module': '<b>• Ping</b>:<code> ping</code>\n'})
