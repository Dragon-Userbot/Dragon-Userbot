from pyrogram import Client, filters
from pyrogram.types import Message
from .utils import utils
from .utils.utils import modules_help, prefix
import asyncio


@Client.on_message(filters.command(['version', 'ver'], prefix) & filters.me)
async def version(client: Client, message: Message):
    changelog = ''
    async for m in client.search_messages('dRaGoN_uB_cHaNgElOg', query=utils.version.split('.')[0]):
        if utils.version in m.text:
            changelog = m.message_id
    await message.delete()
    await message.reply(f'<b>Version</b> <code>{utils.version}</code>.\n'
                       f'<b>Changelog</b> <i><a href=https://t.me/dRaGoN_uB_cHaNgElOg/{changelog}>in channel</a></i>.\n'
                       f'<b>Changelog are written by<a href=tg://user?id=318865588>\u2060</a></b> <a href=tg://user?id=293490416>♿️</a><i><a href=https://t.me/LKRinternationalrunetcomphinc>asphuy</a><a href=https://t.me/artemjj2>♿️</a></i>.')

modules_help.update({'version': '''version - Userbot version and changelog''', 'version module': 'Version: version'})
