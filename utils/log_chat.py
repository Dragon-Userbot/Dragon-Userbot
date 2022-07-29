import os
import asyncio
import logging

from pyrogram.errors import YouBlockedUser, PeerIdInvalid
from pyrogram.types import Message
from utils import config
from .misc import prefix
from .db import db

db.get("core.main", "prefix", ".")

# Log Channel Checker
async def check_or_set_log_channel():
    try:
        al_log_channel =await db.get("core.main", "log_channel_id", "")
        if al_log_channel:
            return [True, al_log_channel]
        else:
            log_channel = await Client.create_channel(title="XUB Bot Logs", description="Logs of your XUB")
            log_channel_id = log_channel.id
            welcome_to_xub = f"""XUB Is done deployed!

{prefix}alive` for check your XUB is alive or not.
"""
            await db.set("core.main", "log_channel_id", f"{log_channel_id}")
            await Client.send_message(chat_id=log_channel_id, text=welcome_to_xub, disable_web_page_preview=True)
            return [True, log_channel_id]
    except Exception as e:
        logging.warn(
            f"Error: \n{e} \n\nPlease check all variables and try again!")
        exit()
