from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import config, config_path, modules_help, prefix
from .utils.scripts import restart
    


@Client.on_message(filters.command(['sp', 'setprefix'], prefix) & filters.me)
async def pref(client: Client, message: Message):
    if len(message.command) > 1:
        prefix = message.command[1]
        print(message.command)
        config.set('prefix', 'prefix', prefix)
        with open(config_path, "w") as config_file:
            config.write(config_file)
        await message.edit(f'<b>Prefix [ <code>{prefix}</code> ] is set!</b>')
        await restart()
    else:
        await message.edit('<b>The prefix must not be empty!</b>')


modules_help.update({'prefix': '''setprefix [prefix]- Set custom prefix''',
                     'prefix module': 'Prefix: setprefix'})
