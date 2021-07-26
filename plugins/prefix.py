from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import config, config_path, modules_help, prefix
from .utils.scripts import restart
    


@Client.on_message(filters.command(['sp', 'setprefix', 'setprefix_dragon'], prefix) & filters.me)
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


modules_help.update({'prefix': f'''setprefix [prefix]\n{prefix}setprefix_dragon [prefix]- Set custom prefix''',
                     'prefix module': 'Prefix: setprefix </code><i>or</i><code> setprefix_dragon'})
