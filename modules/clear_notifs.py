from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.raw import functions, types
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command(["clear_@"], prefix) & filters.me)
async def solo_mention_clear(client: Client, message: Message):
    await message.delete()
    peer = await client.resolve_peer(message.chat.id)
    request = functions.messages.ReadMentions(peer=peer)
    await client.send(request)


@Client.on_message(filters.command(["clear_all_@"], prefix) & filters.me)
async def global_mention_clear(client: Client, message: Message):
    request = functions.messages.GetAllChats(except_ids=[])
    try:
        result = await client.send(request)
    except FloodWait as e:
        await message.edit_text(
            f"<code>FloodWait received. Wait {e.x} seconds before trying again</code>"
        )
        return
    await message.delete()
    for chat in result.chats:
        if type(chat) is types.Chat:
            peer_id = -chat.id
        elif type(chat) is types.Channel:
            peer_id = int(f"-100{chat.id}")
        peer = await client.resolve_peer(peer_id)
        request = functions.messages.ReadMentions(peer=peer)
        await client.send(request)


@Client.on_message(filters.command(["clear_reacts"], prefix) & filters.me)
async def solo_reaction_clear(client: Client, message: Message):
    await message.delete()
    peer = await client.resolve_peer(message.chat.id)
    request = functions.messages.ReadReactions(peer=peer)
    await client.send(request)


@Client.on_message(filters.command(["clear_all_reacts"], prefix) & filters.me)
async def global_reaction_clear(client: Client, message: Message):
    request = functions.messages.GetAllChats(except_ids=[])
    try:
        result = await client.send(request)
    except FloodWait as e:
        await message.edit_text(
            f"<code>FloodWait received. Wait {e.x} seconds before trying again</code>"
        )
        return
    await message.delete()
    for chat in result.chats:
        if type(chat) is types.Chat:
            peer_id = -chat.id
        elif type(chat) is types.Channel:
            peer_id = int(f"-100{chat.id}")
        peer = await client.resolve_peer(peer_id)
        request = functions.messages.ReadReactions(peer=peer)
        await client.send(request)


modules_help["clear_notifs"] = {
    "clear_@": "clear all mentions in this chat",
    "clear_all_@": "clear all mentions in all chats",
    "clear_reacts": "clear all reactions in this chat",
    "clear_all_reacts": "clear all reactions in all chats (except private chats)",
}
