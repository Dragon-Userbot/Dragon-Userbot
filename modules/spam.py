from pyrogram import Message, Filters
from utils import app
import time


@app.on_message(Filters.command('spam', ['.']))
def spam(client, message):
	quantity = message.command[1]
	spam_text = ' '.join(message.command[2:])
	quantity = int(quantity)
	print('spam')
	message.delete()
	for i in range(quantity):
		client.send_message(message.chat.id, spam_text)
		time.sleep(0.2)