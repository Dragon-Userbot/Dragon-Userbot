import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired, RPCError, FloodWait
from utils.misc import modules_help, prefix
from utils.pyrohelpers import get_arg


@Client.on_message(filters.command("invite", prefix) & filters.me & ~filters.private)
async def invite(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("`Who i should invite?`")
            return
    get_user = await client.get_users(user)
    try:
        await client.add_chat_members(message.chat.id, get_user.id)
        await message.edit(f"`{get_user.first_name}` Added to this group.")
    except Exception as e:
        await message.edit(f"{e}")


@Client.on_message(filters.command("inviteall", prefix) & filters.me & ~filters.private)
async def inviteall(client, message):
    nani = await message.edit_text(f"`Give me username or id of group`")
    text = message.text.split(" ", 1)
    ok = text[1]
    chat = await client.get_chat(ok)
    tgchat = message.chat
    om = 0
    am = 0
    await message.edit_text(f"Add member from {chat.username}")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        stats = ["online", "offline", "recently"]
        if user.status in stats:
            try:
                await client.add_chat_members(tgchat.id, user.id, forward_limit=60)
                om = om + 1
                await asyncio.sleep(2)
            except FloodWait as e:
                mg = await client.send_message(client.me.id, f"error-   {e}")
                am = am + 1
                await asyncio.sleep(0.3)
                await mg.delete()
    return await client.send_message(tgchat.id, f"Invite All Modules:\n\n**Succes:** `{om}`\n**Failed:** `{am}`")


@Client.on_message(filters.command("zombies", prefix) & filters.me)
async def zombies(client, message):
    y = await message.edit("processing...")
    ok = 0
    sip = 0
    chat = message.chat.id
    async for klayen in client.get_chat_members(chat):
        if klayen.user.is_deleted:
            ok += 1
    return await y.edit(f"☠️ Deleted account found `{ok}`, `{prefix}zombiesclean` to kick that all.")


@Client.on_message(filters.command("zombiesclean", prefix) & filters.me)
async def terhapus(client, message):
    await message.edit("☠️ Starting cleaning this group...")
    ok = 0
    sip = 0
    chat = message.chat.id
    async for ah in client.get_chat_members(chat):
        if ah.user.is_deleted:
            try:
                await client.ban_chat_member(chat, ah.user.id)
                ok += 1
            except ChatAdminRequired:
                sip += 1
    return await message.edit(f"☠️ Cleaning group...\n**Succes:** `{ok}`\n**Failed:** `{sip}`")


modules_help["mem_tools"] = {
        "invite [username/user_id]": "To invite a user or bot to the chat.",
        "inviteall [chat_username/chat_id]": "To inviting multiple member from chat you want.",
        "zombies": "To checks chat have deleted account member or not.",
        "zombiesclean": "To delete the deleted account from your chat you want.",
}
