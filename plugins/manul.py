from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
import asyncio


@Client.on_message(filters.command('manul', prefix) & filters.me)
async def manul(client: Client, message: Message):
    quantity = message.command[1]
    quantity = int(quantity) + 1
    await message.delete()
    for i in range(1, quantity):
        await client.send_message(message.chat.id, f"{i} манула(ов)")
        await asyncio.sleep(0.2)


modules_help.update(
    {'manul': '''manul [amount of manul] - Release manuls''', 'manul module': 'Manul: manul'})
