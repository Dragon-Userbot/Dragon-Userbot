from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command('support', prefix) & filters.me)
async def support(client: Client, message: Message):
    await message.edit(f'''<b>Channel: @Dragon_Userbot\n\nChat [RU]: @Dragon_Userbot_chat\nChat [EN]: @Dragon_Userbot_chat_en\n\nMain developers: @john_phonk, @LaciaMemeFrame</b>''')

modules_help.update({'support': '''support - Support information''', 'support module': 'Support: support'})
