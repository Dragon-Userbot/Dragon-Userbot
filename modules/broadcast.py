import asyncio
from pyrogram import Client, filters, enums
from requests import get
from utils.misc import modules_help, prefix
from utils.pyrohelpers import get_arg


@Client.on_message(filters.command("gcast", prefix) & filters.me)
async def chat_broadcast(client, message):
    if message.reply_to_message:
        msg = message.reply_to_message
    elif get_arg:
        msg = get_arg(message)
    else:
        return await message.edit_text("Give me a Text/Reply to a message to broadcast it")
    sent = 0
    failed = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
        ]:
            chat = dialog.chat.id
            try:
                await msg.copy(chat)
                sent = sent + 1
                await asyncio.sleep(0.1)
            except:
                failed = failed + 1
                await asyncio.sleep(0.1)
    await message.edit_text(
        f"**Broadcast done!\n\nSucces in:** `{sent}` **Chats\nFailed in:** `{failed}` **Chats**"
    )


@Client.on_message(filters.command("gucast", prefix) & filters.me)
async def chat_broadcast(client, message):
    if message.reply_to_message:
        msg = message.reply_to_message
    elif get_arg:
        msg = get_arg(message)
    else:
        return await message.edit_text("Give me a Text/Reply to a message to broadcast it")
    sent = 0
    failed = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            enums.ChatType.PRIVATE
            ]:
            chat = dialog.chat.id
            try:
                await msg.copy(chat)
                sent = sent + 1
                await asyncio.sleep(0.1)
            except:
                failed = failed + 1
                await asyncio.sleep(0.1)
    await message.edit_text(
        f"**Broadcast Users done!\n\nSucces to:** `{sent}` **Chats\nFailed to:** `{failed}` **Chats**"
    )

modules_help["broadcast"] = {
    "gcast [input/reply]": "To broadcasting a message to your all groups",
    "gucast [input/reply]": "To broadcasting a message to users you have text with them.",
}
