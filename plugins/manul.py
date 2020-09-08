from pyrogram import Client, filters
import time


@Client.on_message(filters.command('manul', ['.']) & filters.me)
def manul(client, message):
	quantity = message.command[1]
	quantity = int(quantity) + 1
	print('manul')
	message.delete()
	for i in range(1, quantity):
		client.send_message(message.chat.id, f"{i} манула(ов)")
		time.sleep(0.2)
