import os
import asyncio
import logging

from pyrogram.errors import YouBlockedUser, PeerIdInvalid
from pyrogram import Client
from utils import config


# Log Channel Checker
async def check_or_set_log_channel():
    try:
        al_log_channel = await get_log_channel()
        if al_log_channel:
            return [True, al_log_channel]
        else:
            log_channel = await NEXAUB.create_channel(title="Nexa Userbot Logs", description="Logs of your Nexa Userbot")
            log_channel_id = log_channel.id
            await NEXAUB.set_chat_photo(chat_id=log_channel_id, photo="cache/NEXAUB.png")
            welcome_to_nexaub = f"""
**Welcome to Nexa Userbot**
Thanks for trying Nexa Userbot. If you found any error, bug or even a Feature Request please report it at **@NexaUB_Support**
**⌲ Quick Start,**
If you don't know how to use this Userbot please send `{Config.CMD_PREFIX}help` in any chat. It'll show all plugins your userbot has. You can use those plugin names to get info about how to use it. Also check out [Docs](https://nexaub.itz-fork.xyz/)
 **~ Nexa Userbot, Developers**"""
            await set_log_channel(log_channel_id)
            await NEXAUB.send_message(chat_id=log_channel_id, text=welcome_to_nexaub, disable_web_page_preview=True)
            return [True, log_channel_id]
    except Exception as e:
        logging.warn(
            f"Error: \n{e} \n\nPlease check all variables and try again! \nReport this with logs at @NexaUB_Support if the problem persists!")
        exit()
