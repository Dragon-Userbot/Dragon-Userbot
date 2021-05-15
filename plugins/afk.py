from pyrogram import Client, filters
from .utils.utils import modules_help
from pyrogram.handlers import MessageHandler
import datetime
import asyncio


async def afk_handler(client, message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = (end - start)
        if message.from_user.is_bot is False:
            await message.reply_text(f"<b>I afk {afk_time}</b>\n"
                                     f"<b>Reason:</b> <i>{reason}</i>")
    except NameError:
        pass


@Client.on_message(filters.command('afk', ['.']) & filters.me)
async def afk(client, message):
    global start, end, handler, reason
    start = datetime.datetime.now().replace(microsecond=0)
    handler = client.add_handler(MessageHandler(afk_handler, (filters.private & ~filters.me)))
    if len(message.text.split()) >= 2:
        reason = message.text.split(" ", maxsplit=1)[1]
    else:
        reason = "еграю"
    await message.edit("<b>I'm going afk</b>")


@Client.on_message(filters.command('unafk', ['.']) & filters.me)
async def unafk(client, message):
    try:
        global start, end
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = (end - start)
        await message.edit(f"<b>I'm not AFK anymore.\nI was afk {afk_time}</b>")
        client.remove_handler(*handler)
    except NameError:
        await message.edit("<b>You weren't afk</b>")
        await asyncio.sleep(3)
        await message.delete()


modules_help.update({'afk': '''<b>Help for |afk|\nUsage:</b>
<code>.afk</code>
<b>[To go to afk]</b>
<code>.unafk</code>
<b>[To get out of AFK]</b>''', 'afk module': '<b>• Afk</b>:<code> afk, unafk</code>\n'})
