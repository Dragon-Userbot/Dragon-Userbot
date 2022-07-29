from pyrogram import Client, filters, errors
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.db import db


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


@Client.on_message(filters.command("gmute", prefix) & filters.me)
async def gmute(client, message):
    if reply := message.reply_to_message:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("<b>Whom should I gmute?</b>")
            return
    get_user = await client.get_users(user)
    gmuted_users = db.get("core.gmute", "gmuted_users", [])
    gmuted_users.append(get_user.id)
    db.set("core.gmute", "gmuted_users", gmuted_users)
    await message.edit(f"<b>Gmuted {get_user.first_name}, LOL!</b>")


@Client.on_message(filters.command("ungmute", prefix) & filters.me)
async def ungmute(client, message):
    if reply := message.reply_to_message:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("<b>Whom should I ungmute?</b>")
            return
    get_user = await client.get_users(user)
    gmuted_users = db.get("core.gmute", "gmuted_users", [])
    try:
        gmuted_users.remove(get_user.id)
    except ValueError:
        pass
    db.set("core.gmute", "gmuted_users", gmuted_users)
    await message.edit(f"<b>Unmuted {get_user.first_name}, enjoy!</b>")


@Client.on_message(filters.group)
async def check_and_del(_, message: Message):
    if message.from_user and message.from_user.id in db.get(
        "core.gmute", "gmuted_users", []
    ):
        try:
            await message.delete()
        except errors.RPCError:
            pass  # you don't have delete rights
    message.continue_propagation()


@Client.on_message(filters.command("gban", prefix) & filters.me)
async def gban(client, message):
    if reply := message.reply_to_message:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("<b>Whom should I gban?</b>")
            return
    get_user = await client.get_users(user)
    gmuted_users = db.get("core.gban", "gbaned_users", [])
    gmuted_users.append(get_user.id)
    db.set("core.gban", "gbaned_users", gbaned_users)
    await message.edit(f"<b>Gbanned {get_user.first_name}, LOL!</b>")


@Client.on_message(filters.command("ungban", prefix) & filters.me)
async def ungban(client, message):
    if reply := message.reply_to_message:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("<b>Whom should I ungban?</b>")
            return
    get_user = await client.get_users(user)
    gmuted_users = db.get("core.gban", "gbaned_users", [])
    try:
        gmuted_users.remove(get_user.id)
    except ValueError:
        pass
    db.set("core.gban", "gbaned_users", gbaned_users)
    await message.edit(f"<b>Ungbanned {get_user.first_name}, enjoy!</b>")


@Client.on_message(filters.group)
async def check_and_del(_, message: Message):
    if message.from_user and message.from_user.id in db.get(
        "core.gmute", "gbaned_users", []
    ):
        try:
            await _.ban_member(message.chat.id, message.from_user.id)
        except errors.RPCError:
            pass  # you don't have delete rights
    message.continue_propagation()


modules_help["gmute"] = {
    "gmute": " global mute of user",
    "ungmute": "unmute user from global ban",
}
