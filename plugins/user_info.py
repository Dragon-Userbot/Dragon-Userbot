from pyrogram import Client, filters
from .utils.utils import modules_help
from pyrogram.raw import functions
from .utils.scripts import date_dict
import time


@Client.on_message(filters.command('inf', ['.']) & filters.me)
def get_user_inf(client, message):
    try:
        user = message.reply_to_message.from_user.id
    except:
        user = message.from_user.id
    user_info = client.send(
        functions.users.GetFullUser(id=client.resolve_peer(user)))
    if user_info.user.username == None:
        username = 'None'
    else:
        username = f'@{user_info.user.username}'
    if user_info.about == None:
        about = 'None'
    else:
        about = user_info.about
    user_info = (f'''|=<b>Username: {username}
|-Id: {user_info.user.id}
|-Bot: {user_info.user.bot}
|-Scam: {user_info.user.scam}
|-Name: {user_info.user.first_name}
|-Deleted: {user_info.user.deleted}
|-BIO: {about}
</b>''')
    message.edit(user_info)


@Client.on_message(filters.command('inffull', ['.']) & filters.me)
def get_full_user_inf(client, message):
    message.edit('<code>Receiving the information...</code>')
    try:
        user = message.reply_to_message.from_user.id
    except:
        user = message.from_user.id
    try:
        client.send_message("@creationdatebot", f"/start")
        time.sleep(1)
        date_dict.clear()
        msg = client.send_message("@creationdatebot", f"/id {user}")
        time.sleep(1)
        client.send(functions.messages.DeleteHistory(peer=client.resolve_peer(747653812), max_id=msg.chat.id))
        user_info = client.send(
            functions.users.GetFullUser(id=client.resolve_peer(user)))
        if user_info.user.username == None:
            username = 'None'
        else:
            username = f'@{user_info.user.username}'
        if user_info.about == None:
            about = 'None'
        else:
            about = user_info.about
        user_info = (f'''|=<b>Username: {username}
|-Id: {user_info.user.id}
|-Account creation date: {date_dict['date']}
|-Bot: {user_info.user.bot}
|-Scam: {user_info.user.scam}
|-Name: {user_info.user.first_name}
|-Deleted: {user_info.user.deleted}
|-BIO: {about}
|-Contact: {user_info.user.contact}
|-Can pin message: {user_info.can_pin_message}
|-Mutual contact: {user_info.user.mutual_contact}
|-Access hash: {user_info.user.access_hash}
|-Restricted: {user_info.user.restricted}
|-Verified: {user_info.user.verified}
|-Phone calls available: {user_info.phone_calls_available}
|-Phone calls private: {user_info.phone_calls_private}
|-Blocked: {user_info.blocked}</b>''')
        date_dict.clear()
        message.edit(user_info)
    except Exception:
        message.edit('<code>An error has occurred...</code>')

modules_help.update({'user_info': '''<b>Help for |User info|\nUsage:</b>
<code>.inf </code>
<b>[Reply to any user message to find out brief information about him]</b>
<code>.inffull </code>
<b>[Reply to any user message to find out full information about him]</b>''', 'user_info module': '<b>• User_info</b>:<code> inf, inffull</code>\n'})
