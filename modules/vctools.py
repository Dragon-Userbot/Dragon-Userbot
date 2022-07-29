import os
from contextlib import suppress
from typing import Optional
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from utils.misc import modules_help, prefix
from utils.scripts import import_library, with_reply, restart

pytgcalls = import_library("pytgcalls")
from pytgcalls import GroupCallFactory

group_call = None


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send_message(message.chat.id, GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send_message(message.chat.id, GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"<b>No group call Found</b> {err_msg}")
    return False


def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


def init_client(func):
    async def wrapper(client, message):
        global group_call
        if not group_call:
            group_call = GroupCallFactory(client).get_file_group_call()
            group_call.enable_logs_to_console = False

        return await func(client, message)

    return wrapper


@Client.on_message(filters.command("play", prefix) & filters.me)
@with_reply
async def start_playout(_, message: Message):
    if not group_call:
        await message.reply(
            f"<b>You are not joined [type <code>{prefix}join</code>]</b>"
        )
        return
    if not message.reply_to_message.audio:
        await message.edit("<b>Reply to a message containing audio</b>")
        return
    input_filename = "input.raw"
    await message.edit("<b>Downloading...</b>")
    audio_original = await message.reply_to_message.download()
    await message.edit("<b>Converting..</b>")
    ffmpeg.input(audio_original).output(
        input_filename, format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(audio_original)
    await message.edit(f"<b>Playing {message.reply_to_message.audio.title}</b>...")
    group_call.input_filename = input_filename


@Client.on_message(filters.command("volume", prefix) & filters.me)
@init_client
async def volume(_, message):
    if len(message.command) < 2:
        await message.edit("<b>You forgot to pass volume [1-200]</b>")
    await group_call.set_my_volume(message.command[1])
    await message.edit(
        f"<b>Your volume is set to</b><code> {message.command[1]}</code>"
    )


@Client.on_message(filters.command("joinvc", prefix) & filters.me)
@init_client
async def joinvc(client: Client, message: Message):
    kontol = get_text(message)
    o = await message.reply("Processing...")
    chat_id = message.chat.id
    if not kontol:
        try:
            await group_call.start(chat_id)
        except Exception as e:
            pass
        await o.edit(f"× Joined VC in: <code>{chat_id}</code>")
    elif kontol:
        try:
            await group_call.start(kontol)
        except Exception as e:
            pass
        await o.edit(f"× Joined VC in: <code>{kontol}</code>")
    await sleep(5)
    await group_call.set_is_mute(True)


@Client.on_message(filters.command("leavevc", prefix) & filters.me)
@init_client
async def stop(_, message: Message):
    try:
        await group_call.stop()
        await message.edit("<b>Leaving successfully!</b>")
    except Exception as e:
        await message.edit(
            f"<b>Аn unexpected error occurred [<code>{e}</code>]\n"
            "The bot will try to exit the voice chat by restarting itself,"
            "the bot will be unavailable for the next 4 seconds</b>"
        )
        restart()

@Client.on_message(filters.command(["startvc"], prefix) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    k = await message.edit("`Processing...`")
    if flags == "channel":
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    try:
        await client.CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
            )
        )
        await k.edit(f"Started group call...")
    except Exception as e:
        await k.edit(f"<b>INFO:</b> <code>{e}</code>")


@Client.on_message(filters.command(["stopvc"], prefix) & filters.me)
async def end_vc_(client: Client, message: Message):
    """End group call"""
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg="group call already ended")
        )
    ):
        return
    await client.DiscardGroupCall(chat_id=chat_id, call=group_call))
    await message.edit("Voice chat ended...")


@Client.on_message(filters.command("stop", prefix) & filters.me)
@init_client
async def stop_playout(_, message: Message):
    group_call.stop_playout()
    await message.edit("<b>Stoping successfully!</b>")


@Client.on_message(filters.command("vmute", prefix) & filters.me)
@init_client
async def mute(_, message: Message):
    group_call.set_is_mute(True)
    await message.edit("<b>Sound off!</b>")


@Client.on_message(filters.command("vunmute", prefix) & filters.me)
@init_client
async def unmute(_, message: Message):
    group_call.set_is_mute(False)
    await message.edit("<b>Sound on!</b>")


@Client.on_message(filters.command("pause", prefix) & filters.me)
@init_client
async def pause(_, message: Message):
    group_call.pause_playout()
    await message.edit("<b>Paused!</b>")


@Client.on_message(filters.command("resume", prefix) & filters.me)
@init_client
async def resume(_, message: Message):
    group_call.resume_playout()
    await message.edit("<b>Resumed!</b>")


modules_help["vctool"] = {
    "play [reply]*": "Play audio in replied message",
    "volume [1 – 200]": "Set the volume level from 1 to 200",
    "joinvc [chat_id]": "Join the voice chat",
    "leavevc": "Leave voice chat",
    "stop": "Stop playback",
    "vmute": "Mute the userbot",
    "vunmute": "Unmute the userbot",
    "pause": "Pause",
    "resume": "Resume",
}
