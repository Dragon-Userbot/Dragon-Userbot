from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, import_library

gTTS = import_library("gtts").gTTS


@Client.on_message(filters.command("tts", prefix) & filters.me)
async def tts(client: Client, message: Message):
    lang = message.command[1]
    text = " ".join(message.command[2:])
    await message.edit("<b>Speech synthesis...</b>")

    try:
        tts = gTTS(text, lang=lang)
        voice = BytesIO()
        tts.write_to_fp(voice)
        voice.name = "voice.ogg"

        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.reply_audio(voice)
        else:
            await client.send_audio(message.chat.id, voice)
    except Exception as e:
        await message.edit(format_exc(e))


modules_help["tts"] = {"tts [lang]* [text]*": "Say text"}
