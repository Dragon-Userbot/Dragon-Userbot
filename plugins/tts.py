from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix

from gtts import gTTS
from io import BytesIO


@Client.on_message(filters.command('tts', prefix) & filters.me)
async def tts(client: Client, message: Message):
    lang = message.command[1]
    text = ' '.join(message.command[2:])
    await message.edit('<code>Speech synthesis...</code>')
    tts = gTTS(text, lang=lang)
    voice = BytesIO()
    tts.write_to_fp(voice)
    voice.name = 'voice.ogg'
    await message.delete()
    if message.reply_to_message:
        await client.send_audio(message.chat.id, voice, reply_to_message_id=message.reply_to_message.message_id)
    else:
        await client.send_audio(message.chat.id, voice)

modules_help.update(
    {'tts': '''tts [lang] [text] - Say text''',
     'tts module': 'Tts: tts'})
