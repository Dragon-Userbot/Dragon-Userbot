#  Dragon-Userbot - telegram userbot
#  Copyright (C) 2020-present Dragon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from io import BytesIO

from gtts import gTTS
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("tts", prefix) & filters.me)
async def tts(client: Client, message: Message):
    lang = message.command[1]
    text = " ".join(message.command[2:])
    await message.edit("<b>Speech synthesis...</b>")
    tts = gTTS(text, lang=lang)
    voice = BytesIO()
    tts.write_to_fp(voice)
    voice.name = "voice.ogg"
    await message.delete()
    if message.reply_to_message:
        await client.send_audio(
            message.chat.id,
            voice,
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_audio(message.chat.id, voice)


modules_help.append({"tts": [{"tts [lang]* [text]*": "Say text"}]})
