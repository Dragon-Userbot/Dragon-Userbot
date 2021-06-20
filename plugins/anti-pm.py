from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from .utils.utils import createDB, modules_help

db = createDB.anti_pm


async def anti_pm_handler(client: Client, message: Message):
    status = await db.find_one({"ANTI_PM": "ENABLE"})
    if status:
        if message.chat.type in ["private"]:
            if not message.from_user.is_contact \
                    and not message.from_user.is_bot:
                await message.delete()


@Client.on_message(filters.command(["anti_pm"], ".") & filters.me)
async def anti_pm(client: Client, message: Message):
    status = await db.find_one({"ANTI_PM": "ENABLE"})
    if status:
        await message.edit("Anti-pm enabled")
        my_handler = MessageHandler(anti_pm_handler)
        client.add_handler(my_handler)
    else:
        antipidoras = {"ANTI_PM": "ENABLE"}
        await db.insert_one(antipidoras)
        my_handler = MessageHandler(anti_pm_handler)
        client.add_handler(my_handler)
        await message.edit("Anti-pm enabled")


@Client.on_message(filters.command(["disable_anti_pm"], ".") & filters.me)
async def disable_anti_pm(client: Client, message: Message):
    status = await db.find_one({"ANTI_PM": "ENABLE"})
    if status:
        await db.delete_one({"ANTI_PM": "ENABLE"})
        await message.edit("Anti-pm disable")
    else:
        await message.edit("Anti-pm disable")


modules_help.update({
                        'antipm': '''anti_pm - Delete all messages from users who are not in the contact book, disable_anti_pm - Disable''',
                        'antipm module': 'AntiPm: anti_pm, '
                                         'disable_anti_pm\n'})
