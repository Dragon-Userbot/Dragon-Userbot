from pyrogram import Message, Filters
from utils import app
import time


@app.on_message(Filters.command('manul', ['.']))
def manul(client, message):
	quantity = message.command[1]
	quantity = int(quantity) + 1
	print('manul')
	message.delete()
	for i in range(1, quantity):
		client.send_message(message.chat.id, f"{i} манула(ов)")
		time.sleep(0.2)
