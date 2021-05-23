from pyrogram import Client, filters
from .utils.utils import modules_help
import re


def text_formatting(module_help, help_type, module_name):
    if help_type == 'all_mods':
        ready_string = f"• <b>{module_help.split(':')[0].strip()}: </b> <code>{module_help.split(':')[1].strip()}</code>\n"
        return ready_string
    elif help_type == 'one_mod':
        s = f'<b>Help for |{module_name}|\nUsage:</b>\n'
        try:
            for i in module_help.split(','):
                command = i.split('-')[0]
                command = re.sub(r"^\s+|\s+$", "", command)
                description = i.split('-')[1]
                description = re.sub(r"^\s+|\s+$", "", description)
                s += f'<code>.{command}</code>\n<b>[{description}]</b>\n'
            return s
        except IndexError:
            return module_help


@Client.on_message(filters.command(['help', 'h'], ['.']) & filters.me)
async def help(client, message):
    module_name = ' '.join(message.command[1:])
    help_message = '''<b>Help for Dragon-Userbot</b>\n<b>For more help on how to use a command, type </b><code>.help |module|</code>\n\n<b>Available Modules:</b>\n'''
    if module_name == '':
        for modules, module_help in sorted(modules_help.items()):
            if modules.endswith(' module'):
                module_help = text_formatting(
                    module_help, help_type='all_mods', module_name=None)
                help_message += module_help

        help_message += f'\n<b>The number of modules in the userbot: {len(modules_help)/2}</b>'
        help_message += f'\n\n<b><a href="https://t.me/Dragon_Userbot">Channel</a> and <a href="https://t.me/Dragon_Userbot_chat">chat</a> in telegram</b>' 
        await message.edit(help_message, parse_mode='html', disable_web_page_preview=True)
    else:
        try:
            text = text_formatting(modules_help[module_name.lower(
            )], help_type='one_mod', module_name=module_name.lower())
            await message.edit(text)
        except KeyError:
            await message.edit(f'<b>Module <code>|{module_name}|</code> not found!</b>')


modules_help.update(
    {'help': '''help |module name| - To get help,
                help - All modules''', 'help module': 'Help: help\n'})
