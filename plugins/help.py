from pyrogram import Client, filters
from .utils.utils import modules_help


@Client.on_message(filters.command('help', ['.']) & filters.me)
def help(client, message):
    module_name = ' '.join(message.command[1:])
    help_message = '''<b>Help for Userbot\nFor more help on how to use a command, type <code>.help |module|</code>\n\nAvailable Modules:\n</b>'''
    if module_name == '':
        for modules, module_help in sorted(modules_help.items()):
            if modules.endswith(' module'):
                help_message += module_help

        help_message += f'\n<b>The number of modules in the userbot: {len(modules_help)/2}</b>'        
        message.edit(help_message, parse_mode='html')
    else:
        try:
            message.edit(modules_help[module_name.lower()])
        except KeyError:
            message.edit(f'<b>Module <code>|{module_name}|</code> not found!</b>')


modules_help.update({'help': '''<b>Help for |help|\nUsage:</b>
<code>.help |module name|</code>
<b>[To get help]</b>''', 'help module': '<b>• Help</b>:<code> help</code>\n'})
