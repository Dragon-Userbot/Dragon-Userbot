from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('repo', ['.']) & filters.me)
def repo(client, message):
    message.edit('My userbot code is <a href=https://github.com/JoHn-111/Userbot>here</a>')


modules_help.update({'repo': '''<b>Help for |repo|\nUsage:</b>
<code>.repo</code>
<b>[Userbot code]</b>''', 'repo module': '<b>• Repo</b>:<code> repo</code>\n'})
