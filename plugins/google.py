from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('google', ["."]) & filters.me)
def webshot(client, message):
    user_request = ' '.join(message.command[1:])

    if user_request == '':
        if message.reply_to_message:
            reply_user_request = message.reply_to_message.text
            request = reply_user_request.replace(' ', '+')
            full_request = f'https://lmgtfy.app/?s=g&iie=1&q={request}'
            message.edit(f'<a href={full_request}>{reply_user_request}</a>')

    else:
        request = user_request.replace(' ', '+')
        full_request = f'https://lmgtfy.app/?s=g&iie=1&q={request}'  
        message.edit(f'<a href={full_request}>{user_request}</a>')


modules_help.update({'google': '''<b>Help for |Google|\nUsage:</b>
<code>.google [request]</code>
<b>[To teach the interlocutor to use Google]</b>
<code>.google</code>
[Answer a stupid question of your interlocutor to teach him how to use Google]''', 'google module': '<b>• Google</b>:<code> google</code>\n'})


