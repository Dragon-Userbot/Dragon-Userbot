import asyncio
from pyrogram.errors.exceptions.bad_request_400 import YouBlockedUser
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteChatUser
from utils.misc import modules_help, prefix
from utils.pyrohelpers import get_arg
from utils.scripts import interact_with, interact_with_to_delete, format_exc


@Client.on_message(filters.command(["sg", "sa"], prefix) & filters.me)
async def sangmata(client, message):
    await message.edit_text("Processing")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.edit_text("Can't fint histroy name.")
        return
    bot = "SangMataInfo_bot"
    chat = message.chat.id
    if user:
        try:
            y = await client.send_message(bot, f"/search_id {user.id}")
            await sleep(1)
            await y.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            y = await client.send_message(bot, f"/search_id {user.id}")
            await sleep(1)
            await y.delete()
            return
    elif cmd[1]:
        try:
            y = await client.send_message(bot, f"/search_id {cmd[1]}")            await sleep(1)
            await y.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            y = await client.send_message(bot, f"/search_id {user.id}")
            await sleep(1)
            await y.delete()
            return
    async for jembut in client.search_messages(bot, query="Name", limit=1):
        if not jembut:
            await message.edit_text("Can't find histroy name of that user.")
            return
        elif jembut:
            iss = jembut.text
            await y.delete()
            await message.edit(iss)
            await jembut.delete()


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
        except YouBlockedUser:
            await client.unblock_user(bot)
            y = await client.send_message(bot, tetek)
            await asyncio.sleep(5)
            await y.delete()
    async for turok in client.search_messages(bot, filter=enums.MessagesFilter.VIDEO, limit=1):
        await client.send_video(chat, video=turok.video.file_id, caption=f"**Upload by:** [{pop}](tg://user?id={ah})")
        await uh.delete()
        await turok.delete()
        await client.delete_messages(bot, 2)


modules_help["extras"] = {
    "tt [link|reply]*": "Download video from tiktok",
    "sg [id|reply]*": "Check history name of user",
}
