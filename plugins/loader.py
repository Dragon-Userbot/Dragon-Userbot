from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from .utils.scripts import restart
import requests
import os


@Client.on_message(filters.command(['loadmod', 'lm'], prefix) & filters.me)
async def load_mods(client: Client, message: Message):
    if len(message.command) > 1:
        url = message.command[1]
        if '/'.join(url.split('/')[:6]) == 'https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main':
            if not os.path.exists(f'{os.path.abspath(os.getcwd())}/plugins/custom_modules'):
                os.mkdir(
                    f'{os.path.abspath(os.getcwd())}/plugins/custom_modules')

            with open(f'./plugins/custom_modules/{url.split("/")[6]}', 'wb') as mod:
                code = requests.get(url)
                mod.write(code.content)
            await message.edit(f'<b>The module <code>{url.split("/")[6].split(".")[0]}</code> is loaded!</b>')
            await restart()
        else:
            await message.edit('<b>Only modules from the official <a href=https://github.com/Dragon-Userbot/custom_modules>custom_modules</a> repository are supported!</b>',
                               disable_web_page_preview=True)


@Client.on_message(filters.command(['unloadmod', 'ulm'], prefix) & filters.me)
async def unload_mods(client: Client, message: Message):
    if len(message.command) > 1:
        mod = message.command[1]
        if '/'.join(mod.split('/')[:6]) == 'https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main':
            mod = '/'.join(mod.split('/')[6:]).split('.')[0]

        if os.path.exists(f'{os.path.abspath(os.getcwd())}/plugins/custom_modules/{mod}.py'):
            os.remove(
                f'{os.path.abspath(os.getcwd())}/plugins/custom_modules/{mod}.py')
            await message.edit(f'<b>The module <code>{mod}</code> removed!</b>')
            await restart()

        elif os.path.exists(f'{os.path.abspath(os.getcwd())}/plugins/{mod}.py'):
            await message.edit(f'<b>It is forbidden to remove built-in modules, it will disrupt the updater</b>')

        else:
            await message.edit(f'<b>Module <code>{mod}</code> not found</b>')


modules_help.update(
    {'loader': '''loadmod [link] - Download module]\n[Only modules from the official custom_modules repository are supported, 
                  unloadmod [module_name] - Delete module''',
    'loader module': 'Loader: loadmod, unloadmod'})
