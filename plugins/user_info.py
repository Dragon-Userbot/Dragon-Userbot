from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from pyrogram.raw import functions
from .utils.scripts import date_dict
import asyncio


@Client.on_message(filters.command('inf', prefix) & filters.me)
async def get_user_inf(client: Client, message: Message):
    try:
        user = message.reply_to_message.from_user.id
    except:
        user = message.from_user.id
    user_info = await client.send(
        functions.users.GetFullUser(id=await client.resolve_peer(user)))
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
    await message.edit(user_info)


@Client.on_message(filters.command('inffull', prefix) & filters.me)
async def get_full_user_inf(client: Client, message: Message):
    await message.edit('<code>Receiving the information...</code>')
    try:
        user = message.reply_to_message.from_user.id
    except:
        user = message.from_user.id
    try:
        await client.send_message("@creationdatebot", f"/start")
        await asyncio.sleep(1)
        date_dict.clear()
        msg = await client.send_message("@creationdatebot", f"/id {user}")
        await asyncio.sleep(1)
        await client.send(functions.messages.DeleteHistory(peer=await client.resolve_peer(747653812), max_id=msg.chat.id))
        user_info = await client.send(
            functions.users.GetFullUser(id=await client.resolve_peer(user)))
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
        await message.edit(user_info)
    except:
        await message.edit('<code>An error has occurred...</code>')

modules_help.update({'user_info': '''inf - Reply to any user message to find out brief information about him,
                                     inffull - Reply to any user message to find out full information about him''',
                     'user_info module': 'User_info: inf, inffull'})
