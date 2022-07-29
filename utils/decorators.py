import traceback
from typing import Union
from functools import wraps
from pyrogram.types import Message, InlineQuery, CallbackQuery
from pyrogram import Client, StopPropagation, ContinuePropagation
from pyrogram.errors import (
    MessageEmpty, MessageIdInvalid, BotInlineDisabled, MessageNotModified,
    UserNotParticipant)
from main import bot
import asyncio


async def set_inline_in_botfather(Client: client):
    message = await Client.send_message("botfather", "/setinline")
    await asyncio.sleep(1)
    await message.reply(f"@{bot.username}")


def inline_check(func):
    @wraps(func)
    async def check_inline(c: Client, m: Message, *args, **kwargs):
        try:
            return await func(c, m)
        except BotInlineDisabled:
            status = await m.handle_message("INLINE_DISABLED")
            await set_inline_in_botfather(c)
            await status.delete()
            return await func(c, m)

    return check_inline
