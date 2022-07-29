import shlex
from pyrogram import Client
from pyrogram.types import Message
from enum import IntEnum, unique
from pyrogram.types import Message
from pyrogram import enums


async def eor(message: Message, *args, **kwargs) -> Message:
    ok = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await ok(*args, **kwargs)


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def get_args(message):
    try:
        message = message.text
    except AttributeError:
        pass
    if not message:
        return False
    message = message.split(maxsplit=1)
    if len(message) <= 1:
        return []
    message = message[1]
    try:
        split = shlex.split(message)
    except ValueError:
        return message  # Cannot split, let's assume that it's just one long message
    return list(filter(lambda x: len(x) > 0, split))


def ReplyCheck(message: Message):
    reply_id = None
    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id
    elif not message.from_user.is_self:
        reply_id = message.message_id
    return reply_id
