from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command('webshot', prefix) & filters.me)
async def webshot(client: Client, message: Message):
    try:
        user_link = message.command[1]
        await message.delete()
        full_link = f'https://webshot.deam.io/{user_link}/?delay=2000'
        await client.send_document(message.chat.id, full_link, caption=f'{user_link}')
    except:
        await message.delete()
        await client.send_message(message.chat.id, '<code>Something went wrong...</code>')


modules_help.update({'webshot': '''webshot [link to the page] - Screenshot of web page''',
                     'webshot module': 'Webshot: webshot'})
