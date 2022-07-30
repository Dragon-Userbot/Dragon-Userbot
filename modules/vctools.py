from asyncio import sleep
from contextlib import suppress
from random import randint
from typing import Optional
from pyrogram import Client, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from utils.misc import modules_help, prefix


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.reply(f"**No group call Found** {err_msg}")
    return False


@Client.on_message(filters.command(["startvc"], prefix) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    Cilik = await message.edit("`Processing...`")
    if flags == "channel":
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    try:
        await client.send(
            CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
            )
        )
        await Cilik.edit(f"Started group call in **Chat ID** : `{chat_id}`")
    except Exception as e:
        await Cilik.edit(f"**INFO:** `{e}`")


@Client.on_message(filters.command(["stopvc"], prefix) & filters.me)
async def end_vc_(client: Client, message: Message):
    """End group call"""
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", group call already ended")
        )
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await message.edit(f"Ended group call in **Chat ID** : `{chat_id}`")


@Client.on_message(filters.command("joinvc", prefix) & filters.me)
async def joinvc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        pepek = await message.edit("`Processing...`")
    else:
        pepek = await message.edit("`Processing...`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.start(chat_id)
    except Exception as e:
        return await pepek.edit(f"**ERROR:** `{e}`")
    await pepem.edit(f"Joined to VoiceChat `{chat_id}`")
    await sleep(5)
    await client.group_call.set_is_mute(True)


@Client.on_message(filters.command("leavevc", prefix) & filters.me)
async def leavevc(client: Client, message: Message):
    try:
        await client.group_call.stop()
    except Exception as e:
        return await message.edit(f"**ERROR:** `{e}`")
    await message.edit(
        f"Leaved to VoiceChat `{message.chat.id}`"
    )


modules_help["vctools"] = {
    "startvc": "Starting video calls",
    "stopvc": "Stop the vidro calls",
    "joinvc": "Joining video calls",
    "leavevc": "Leave the video calls",
}
