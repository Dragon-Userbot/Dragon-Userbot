from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command(['help', 'h'], ['.']) & filters.me)
async def help(client, message):
    module_name = ' '.join(message.command[1:])
    help_message = '''<b>Help for Dragon-Userbot</b>\n<b>For more help on how to use a command, type </b><code>.help |module|</code>\n\n<b>Available Modules:</b>\n'''
    if module_name == '':
        for modules, module_help in sorted(modules_help.items()):
            if modules.endswith(' module'):
                help_message += module_help

        help_message += f'\n<b>The number of modules in the userbot: {len(modules_help)/2}</b>'
        help_message += f'\n\n<b><a href="https://t.me/Dragon_Userbot">Channel</a> and <a href="https://t.me/Dragon_Userbot_chat">chat</a> in telegram</b>' 
        await message.edit(help_message, parse_mode='html', disable_web_page_preview=True)
    else:
        try:
            await message.edit(modules_help[module_name.lower()])
        except KeyError:
            await message.edit(f'<b>Module <code>|{module_name}|</code> not found!</b>')


modules_help.update({'help': '''<b>Help for |help|\nUsage:</b>
<code>.help |module name|</code>
<b>[To get help]</b>''', 'help module': '<b>• Help</b>:<code> help</code>\n'})
