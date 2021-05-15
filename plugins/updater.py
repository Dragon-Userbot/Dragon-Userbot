from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help
import subprocess
from .utils.utils import requirements_list
import asyncio


async def restart(client: Client, message: Message):
    await client.restart(block=False)
    await message.edit('<code>Restart was successful!</code>')
    
    
async def update_restart(client: Client, message: Message):
    await client.restart(block=False)
    await message.edit('<code>Restart was successful!</code>')
    await asyncio.sleep(3)
    await message.edit('<code>Update process completed!</code>')
    
@Client.on_message(filters.command('restart', ['.']) & filters.me)
async def restart_comand(client: Client, message: Message):
    await message.edit('<code>Restarting...</code>')
    import asyncio
    asyncio.get_event_loop().create_task(restart(client, message))
    
@Client.on_message(filters.command('update', ["."]) & filters.me)
async def update(client: Client, message: Message):
    await message.edit('<code>Updating...</code>')
    pip_update = subprocess.Popen(["python3", "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.PIPE)
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    for lib in range(len(requirements_list)):
        process = subprocess.Popen(["pip3", "install", "-U", f"{requirements_list[lib]}"], stdout=subprocess.PIPE)
        output = process.communicate()[0]
    await message.edit('<code>Restarting...</code>')
    import asyncio
    asyncio.get_event_loop().create_task(update_restart(client, message)) 
    
modules_help.update({'updater': '''<b>Help for |Updater|\nUsage:</b>
<code>.update</code>
<b>[Updating the userbot. If new modules are available, they will be installed]</b>
<code>.restart</code>
<b>[Restart userbot]</b>''', 'updater module': '<b>• Updater</b>:<code> update, restart</code>\n'})
