from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command(['say', 's'], prefix) & filters.me)
async def say(client: Client, message: Message):
    if len(message.command) == 1:
        return
    command = ' '.join(message.command[1:])
    await message.edit(f'<code>{command}</code>')
    

modules_help.update({'say': '''say [command] - Show the command to the interlocutor''',
                     'say module': 'Say: say'})
