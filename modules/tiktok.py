from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import interact_with, interact_with_to_delete, format_exc


import asyncio
import random
from asyncio import sleep
from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.errors import RPCError
from pyrogram.errors import PeerIdInvalid
from utils.pyrohelpers import get_arg


@Client.on_message(filters.command("limit", prefix) & filters.me)
async def limit(client, message):
    a = await message.edit_text("Processing")
    chat = message.chat.id
    bot = "SpamBot"
    try:
        ok = await app.send_message(bot, "/start")
        await ok.delete()
    except RPCError:
        await a.edit_text(f"Please unblock @{bot} first!")
        return
    async for sip in client.get_chat_history(bot, limit=1):
        if not sip:
            await message.edit_text("Something went wrong!")
        elif jembut:
            oh = sip.text
            await a.edit(oh)
            await sip.delete()


@Client.on_message(filters.command("json", prefix) & filters.me)
async def showjson(client, message):
    try:
        if message.reply_to_message:
            msg = message.reply_to_message
        else:
            msg = message
        msg_info = str(msg)
        if len(msg_info) > int("4096"):
            file = open("json.txt", "w+")
            file.write(msg_info)
            file.close()
            await client.send_document(
                message.chat.id,
                "json.txt",
                caption="Returned JSon",
            )
            remove("json.txt")
        else:
            await message.edit(msg_info)
    except Exception as e:
        await message.edit(f"{e}")


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
        await message.edit_text("I doubt that a user.")
        return
    bot = "SangMataInfo_bot"
    chat = message.chat.id
    if user:
        try:
            y = await client.send_message(bot, f"/search_id {user.id}")
            await sleep(1)
            await y.delete()
        except RPCError:
            await message.edit(f"Please unblock @{bot} first!")
            return
    elif cmd[1]:
        try:
            y = await client.send_message(bot, f"/search_id {cmd[1]}")            
            await sleep(1)
            await y.delete()
        except RPCError:
            await message.edit(f"Please unblock @{bot} first!")
            return
    async for oke in client.search_messages(bot, query="Name", limit=1):
        if not oke:
            await message.edit_text("Can't find history name that users.")
            return
        elif oke:
            nah = oke.text
            await y.delete()
            await message.edit(nah)
            await oke.delete()


@Client.on_message(filters.command("tt", prefix) & filters.me)
async def sosmed(client, message):
    y = await message.edit("Processing")
    query = get_arg(message)
    chat = message.chat.id
    pop = message.from_user.first_name
    ah = message.from_user.mention
    bot = "thisvidbot"
    if query:
        try:
            await client.send_message(bot, query)
            await asyncio.sleep(5)
        except RPCError:
            return await message.edit(f"Please unblock @{bot} first!")
    async for yare in client.search_messages(bot, filter=enums.MessagesFilter.VIDEO, limit=1):
        await client.send_video(chat, video=yare.video.file_id)
        await y.delete()
        await yare.delete()


modules_help["extras"] = {
    "tt [link|reply]*": "Download video from tiktok",
    "sg or sa [id|reply]*": "Get history name user",
    "json [reply]": "Show json text",
    "limit": "Show account status on @spambot",
}
