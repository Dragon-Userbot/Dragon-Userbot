from pyrogram import Client, filters
from .utils.utils import modules_help, prefix
from .utils.help_formatting import help_formatting


@Client.on_message(filters.command(['help', 'h'], prefix) & filters.me)
async def help(client, message):
    module_name = ' '.join(message.command[1:])
    help_message = f'''<b>Help for Dragon-Userbot</b>\n<b>For more help on how to use a command, type </b> <code>{prefix}help |module|</code>\n'''
    help_message += f'<b>The prefix has the value [ <code>{prefix}</code> ]</b>\n\n'
    help_message += '<b>Available Modules:</b>\n'
    if module_name == '':
        for modules, module_help in sorted(modules_help.items()):
            if modules.endswith(' module'):
                module_help = help_formatting(
                    module_help, help_type='all_mods', module_name=None)
                help_message += module_help

        help_message += f'\n<b>The number of modules in the userbot: {len(modules_help)/2}</b>'
        help_message += f'\n\n<b><a href="https://t.me/Dragon_Userbot">Channel</a> and <a href="https://t.me/Dragon_Userbot_chat">chat</a> in telegram</b>' 
        await message.edit(help_message, parse_mode='HTML', disable_web_page_preview=True)
    else:
        try:
            text = help_formatting(modules_help[module_name.lower(
            )], help_type='one_mod', module_name=module_name.lower())
            await message.edit(text, parse_mode='HTML')
        except KeyError:
            await message.edit(f'<b>Module <code>|{module_name}|</code> not found!</b>')


modules_help.update(
    {'help': '''help |module name| - To get help,
                help - All modules''', 'help module': 'Help: help\n'})
