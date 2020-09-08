from pyrogram import Client, filters


@Client.on_message(filters.command('repo', ['.']) & filters.me)
def repo(client, message):
    message.edit('My userbot code is <a href=https://github.com/JoHn-111/Userbot>here</a>')
