from pyrogram import Client, filters
from pyrogram.types import Message
import os

date_dict = {}

@Client.on_message(filters.chat("@creationdatebot"), group=-1)
async def get_date(client: Client, message: Message):
    await client.read_history("@creationdatebot")
    date_dict.update({"date": message.text})

async def restart():
    await os.execvp("python3", ["python3", "main.py"])