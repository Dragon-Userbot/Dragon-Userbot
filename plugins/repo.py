from pyrogram import Client, filters
from .utils import utils
from .utils.utils import modules_help


@Client.on_message(filters.command('repo', ['.']) & filters.me)
async def repo(client, message):
    await message.edit(f'''<b>---Dragon-Userbot---
• Userbot on{utils.github}
• License: {utils.license}
• Copyright: {utils.copyright}
• Python version: {utils.python_version}
• Number of modules: {len(modules_help)/2}</b>''')


utils.modules_help.update({'repo': '''<b>Help for |repo|\nUsage:</b>
<code>.repo</code>
<b>[Userbot information]</b>''', 'repo module': '<b>• Repo</b>:<code> repo</code>\n'})
