import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.pyrohelpers import get_arg
from utils.scripts import interact_with, interact_with_to_delete, format_exc


@Client.on_message(filters.command("tt", prefix) & filters.me)
async def sosmed(client, message):
    uh = await message.edit("Processing")
    tetek = get_arg(message)
    chat = message.chat.id
    pop = message.from_user.first_name
    ah = message.from_user.id
    bot = "thisvidbot"
    if tetek:
        try:
            y = await client.send_message(bot, tetek)
            await asyncio.sleep(5)
            await y.delete()
        except Exception as e:
            return await client.send_message(client.me.id, f"{e}")
    async for turok in client.search_messages(bot, filter=enums.MessagesFilter.EMPTY, limit=2):
        await client.send_video(chat, video=turok.video.file_id, caption=f"**Upload by:** [{pop}](tg://user?id={ah})")
        await uh.delete()
        await turok.delete()


modules_help["tiktok"] = {
    "tt [link|reply]*": "download video from tiktok",
}
