from pyrogram import Client, filters
from pyrogram.types import Message
from .utils import utils
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command('repo', prefix) & filters.me)
async def repo(client: Client, message: Message):
    await message.edit(f'''<b>---Dragon-Userbot---
• Userbot on{utils.github}
• License: {utils.license}
• Copyright: {utils.copyright}
• Python version: {utils.python_version}
• Number of modules: {len(modules_help)/2}
• <a href="https://t.me/Dragon_Userbot">Channel</a> and <a href="https://t.me/Dragon_Userbot_chat">chat</a> in telegram</b>''', disable_web_page_preview=True)


utils.modules_help.update({'repo': '''repo - Userbot information''', 'repo module': 'Repo: repo'})
