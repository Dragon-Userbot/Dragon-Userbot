from pyrogram.types import Message
from pyrogram import Client, filters


@Client.on_message(filters.command('inf', ['.']) & filters.me)
def get_user_inf(client, message):
	user = message.reply_to_message.from_user.username
	print(user)
	user_info = client.get_users(user)
	print(user_info)
	user_info = (f'''|=<b>Username: @{user_info.username}
|-Id: {user_info.id}
|-Bot: {user_info.is_bot}
|-Scam: {user_info.is_scam}
|-Name: {user_info.first_name}
|-Status: {user_info.status}
|-Deleted: {user_info.is_deleted}
</b>''')
	message.edit(user_info)