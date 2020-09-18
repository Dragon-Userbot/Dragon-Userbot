from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('webshot', ["."]) & filters.me)
def webshot(client, message):
    user_link = message.command[1]
    message.delete()
    full_link = f'https://webshot.deam.io/{user_link}/?width=1920&height=1080?type=png'
    try:
        client.send_document(message.chat.id, full_link, caption=f'{user_link}')
    except:
        pass


modules_help.update({'webshot': '''<b>Help for |Webshot|\nUsage:</b>
<code>.webshot [link to the page]</code>
<b>[Screenshot of web page]</b>''', 'webshot module': '<b>• Webshot</b>:<code> webshot</code>\n'})