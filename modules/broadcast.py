import asyncio
from pyrogram import Client, filters, enums
from requests import get
from utils.misc import modules_help, prefix
from utils.pyrohelpers import get_arg
from pyrogram.errors import FloodWait
from pyrogram.types import Message


@Client.on_message(filters.command("gcast", prefix) & filters.me)
async def gcast(client: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        msg = message.reply_to_message
        yanto = await message.edit("`Global Broadcasting!`")
        sent = 0
        failed = 0
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                "supergroup",
                "group",
            ]:
                chat = dialog.chat.id
                try:
                    await msg.copy(chat)
                    sent = sent + 1
                    await asyncio.sleep(0.1)
                except:
                    failed = failed + 1
                    await asyncio.sleep(0.1)
            await yanto.edit_text(
                f"Done in {sent} chats, error in {failed} chat(s)"
            )
        return
    if len(message.command) < 2:
        await message.edit(
             "`Reply or give text to broadcast.`"
        )
        return
    yanto = await message.edit("`Global Broadcasting!`")
    panjul = message.text.split(None, 1)[1]
    sent = 0
    failed = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
             "supergroup",
             "group",
        ]:
             chat = dialog.chat.id
             try:
                 await client.send_message(chat, text=panjul)
                 sent = sent + 1
                 await asyncio.sleep(0.1)
             except:
                 failed = failed + 1
                 await asyncio.sleep(0.1)
    return await yanto.edit_text(
        f"Done in {sent} chats, error in {failed} chat(s)"
    )


@Client.on_message(filters.command("gucast", prefix) & filters.me)
async def gucast(client: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        msg = message.reply_to_message
        yanto = await message.edit("`Global Broadcasting to users!`")
        sent = 0
        failed = 0
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                "private",
            ]:
                chat = dialog.chat.id
                try:
                    await msg.copy(chat)
                    sent = sent + 1
                    await asyncio.sleep(0.1)
                except:
                    failed = failed + 1
                    await asyncio.sleep(0.1)
                await yanto.edit_text(
                    f"✅ **Gucast Successfully\nSend to:** {sent} **Chats\n Failed to send :** {failed} **Chats**"
                )
        return
    if len(message.command) < 2:
        await message.edit(
             "`Give a text or reply to broadcast.`"
        )
        return
    yanto = await message.reply_text("`Global Broadcasting to users!`")
    panjul = message.text.split(None, 1)[1]
    sent = 0
    failed = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
             "private",
        ]:
             chat = dialog.chat.id
             try:
                 await client.send_message(chat, text=panjul)
                 sent = sent + 1
                 await asyncio.sleep(0.1)
             except:
                 failed = failed + 1
                 await asyncio.sleep(0.1)
             await yanto.edit_text(
                 f"**✅ Gucast Successfully\nSend to:** {sent} **Chats\n Failed to send :** {failed} **Chats**"
             )


modules_help["broadcast"] = {
    "gcast [input/reply]": "To broadcasting a message to your all groups",
    "gucast [input/reply]": "To broadcasting a message to users you have text with them.",
}
