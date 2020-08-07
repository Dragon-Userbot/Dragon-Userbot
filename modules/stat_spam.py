from pyrogram import Message, Filters
from utils import app
import time


@app.on_message(Filters.command('stspam', ['.']))
def stat_spam(client, message):
	quantity = message.command[1]
	spam_text = ' '.join(message.command[2:])
	quantity = int(quantity)
	print('stat_spam')
	message.delete()
	for i in range(quantity):
		client.send_message(message.chat.id, spam_text)
		time.sleep(2)
		message.delete(message.message_id)
		print(message)
		#print(client.delete_messages(message.chat.id, message.message_id))
		print(message.delete(message))
		#client.delete_messages(message.chat.id, message.message_id)
		print('2')
		time.sleep(0.2)