from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help


@Client.on_message(filters.command('webshot', ["."]) & filters.me)
async def webshot(client: Client, message: Message):
    try:
        user_link = message.command[1]
        await message.delete()
        full_link = f'https://webshot.deam.io/{user_link}/?delay=2000'
        await client.send_document(message.chat.id, full_link, caption=f'{user_link}')
    except:
        await message.delete()
        await client.send_message(message.chat.id, '<code>Something went wrong...</code>')


modules_help.update({'webshot': '''<b>Help for |Webshot|\nUsage:</b>
<code>.webshot [link to the page]</code>
<b>[Screenshot of web page]</b>''', 'webshot module': '<b>• Webshot</b>:<code> webshot</code>\n'})
