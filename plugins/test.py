from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('test', ['.']) & filters.me)
def test_func(client, message):
	message.edit('test')