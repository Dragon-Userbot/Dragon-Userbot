from pyrogram.types import Message
from pyrogram import Client, filters


@Client.on_message(filters.command('inf', ['.']) & filters.me)
def get_user_inf(client, message):
    user = message.reply_to_message.from_user.id
    user_info = client.get_users(user)
    if user_info.username == None:
        username = 'None'
    else:
        username = f'@{user_info.username}'
    user_info = (f'''|=<b>Username: {username}
|-Id: {user_info.id}
|-Bot: {user_info.is_bot}
|-Scam: {user_info.is_scam}
|-Name: {user_info.first_name}
|-Status: {user_info.status}
|-Deleted: {user_info.is_deleted}
</b>''')
    message.edit(user_info)
