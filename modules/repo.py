from pyrogram import Message, Filters
from utils import app


@app.on_message(Filters.command('repo', ['.']) & Filters.me)
def repo(client, message):
    message.edit('My userbot code is <a href=https://github.com/JoHn-111/Userbot>here</a>')