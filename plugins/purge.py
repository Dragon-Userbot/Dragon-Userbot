from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('del', ["."]) & filters.me)
def del_msg(client, message):
    if message.reply_to_message:
        message_id = message.reply_to_message.message_id
        message.delete()
        client.delete_messages(message.chat.id, message_id)


@Client.on_message(filters.command('purge', ["."]) & filters.me)
def purge(client, message):
    if message.reply_to_message:
        start_message = message.reply_to_message.message_id
        end_message = message.message_id
        message_ids = range(start_message, end_message)
        messages = client.get_messages(chat_id=message.chat.id, message_ids=message_ids, replies=0)
        messages_list = []
        quantity = 0
        for message_iter in messages:
            if len(messages_list) == 100:
                client.delete_messages(chat_id=message.chat.id, message_ids=message_ids)
            else:
                messages_list.append(message_iter.message_id)

        if messages_list:
            client.delete_messages(chat_id=message.chat.id,message_ids=messages_list)

        message.edit('<b>Сleaning was successful!</b>')
    else:
        message.edit('<b>Reply to a message after which you want to delete messages</b>')


modules_help.update({'purge': '''<b>Help for |purge|\nUsage:</b>
<code>.purge</code>
<b>[Reply to a message after which you want to delete messages]
<code>.del</code>
[Reply to the message you want to delete]</b>''', 'purge module': '<b>• Purge</b>:<code> purge, del</code>\n'})