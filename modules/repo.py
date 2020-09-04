from pyrogram.types import Message
from pyrogram import filters
from utils import app


@app.on_message(filters.command('repo', ['.']) & filters.me)
def repo(client, message):
    message.edit('My userbot code is <a href=https://github.com/JoHn-111/Userbot>here</a>')
