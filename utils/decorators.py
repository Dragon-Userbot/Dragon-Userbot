import traceback
from typing import Union
from functools import wraps
from utils.bot.set_inline import set_inline_in_botfather
from pyrogram.types import Message, InlineQuery, CallbackQuery
from pyrogram import Client, StopPropagation, ContinuePropagation
from pyrogram.errors import (
    MessageEmpty, MessageIdInvalid, BotInlineDisabled, MessageNotModified,
    UserNotParticipant)


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
