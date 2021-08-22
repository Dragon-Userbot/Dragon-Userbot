from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from pyrogram.errors import UserAdminInvalid, ChatAdminRequired, PeerIdInvalid, UsernameInvalid
from pyrogram.raw import functions
from pyrogram.handlers import MessageHandler
from .utils.utils import createDB, modules_help, prefix
from .utils.scripts import text, chat_permissions
from time import time
import re
from typing import Dict

db = createDB.admin_tool


async def restrict_users_in_tmute(client: Client, message: Message):
    if message.from_user:
        user = await db.find_one({"USER_ID": f"{message.from_user.id}",
                                 "CHAT_ID": f"{message.chat.id}"})
        if user:
            await message.delete()


@Client.on_message(filters.command(["ban"], prefix) & filters.me)
async def ban_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(message.reply_to_message.from_user.id)
                if "report_spam" in cause.lower().split():
                    await client.send(functions.channels.ReportSpam(channel=(channel),
                                                                user_id=(user_id),
                                                                id=[message.reply_to_message.message_id]))
                if "delete_history" in cause.lower().split():
                    await client.send(functions.channels.DeleteUserHistory(channel=(channel),
                                                                           user_id=(user_id)))
                text_c = ""
                for _ in cause.split():
                    if _.lower() != "delete_history" and _.lower() != "report_spam":
                        text_c += f" {_}"
                await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>banned!</code>"
                                   + f"\n{'<b>Cause:</b> <i>' + text_c.split(maxsplit=1)[1] + '</i>' if len(text_c.split()) > 1 else ''}")
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                user_to_ban = await client.get_users(cause.split(" ")[1])
                try:
                    await client.kick_chat_member(message.chat.id, user_to_ban.id)
                    await message.edit(f"<b>{user_to_ban.first_name}</b> <code>banned!</code>"
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["unban"], prefix) & filters.me)
async def unban_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>unbanned!</code>"
                                   + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}")
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                user_to_unban = await client.get_users(cause.split(" ")[1])
                try:
                    await client.unban_chat_member(message.chat.id, user_to_unban.id)
                    await message.edit(f"<b>{user_to_unban.first_name}</b> <code>unbanned!</code>"
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["kick"], prefix) & filters.me)
async def kick_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                await client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(message.reply_to_message.from_user.id)
                if "report_spam" in cause.lower().split():
                    await client.send(functions.channels.ReportSpam(channel=(channel),
                                                                user_id=(user_id),
                                                                id=[message.reply_to_message.message_id]))
                if "delete_history" in cause.lower().split():
                    await client.send(functions.channels.DeleteUserHistory(channel=(channel),
                                                                           user_id=(user_id)))
                text_c = ""
                for _ in cause.split():
                    if _.lower() != "delete_history" and _.lower() != "report_spam":
                        text_c += f" {_}"
                await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>kicked!</code>"
                                   + f"\n{'<b>Cause:</b> <i>' + text_c.split(maxsplit=1)[1] + '</i>' if len(text_c.split()) > 1 else ''}")
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                user_to_ban = await client.get_users(cause.split(" ")[1])
                try:
                    await client.kick_chat_member(message.chat.id, user_to_ban.id)
                    await client.unban_chat_member(message.chat.id, user_to_ban.id)
                    await message.edit(f"<b>{user_to_ban.first_name}</b> <code>kicked!</code>"
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tmute"], prefix) & filters.me)
async def tmute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            if not message.reply_to_message.from_user.is_self:
                find_user = await db.find_one({"USER_ID": f"{message.reply_to_message.from_user.id}",
                                               "CHAT_ID": f"{message.chat.id}"})
                if not find_user:
                    await db.insert_one({"USER_ID": f"{message.reply_to_message.from_user.id}",
                                        "CHAT_ID": f"{message.chat.id}"})
                    await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>in tmute</code>"
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}")
                    client.add_handler(MessageHandler(restrict_users_in_tmute, filters.group))
                else:
                    await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>already in tmute</code>")
                    client.add_handler(MessageHandler(restrict_users_in_tmute, filters.group))
            else:
                await message.edit("<b>Not on yourself</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                user_to_tmute = await client.get_users(cause.split(" ")[1])
                if not user_to_tmute.is_self:
                    find_user = await db.find_one({"USER_ID": f"{user_to_tmute.id}",
                                                   "CHAT_ID": f"{message.chat.id}"})
                    if not find_user:
                        await db.insert_one({"USER_ID": f"{user_to_tmute.id}",
                                             "CHAT_ID": f"{message.chat.id}"})
                        client.add_handler(MessageHandler(restrict_users_in_tmute, filters.group))
                        await message.edit(f"<b>{user_to_tmute.first_name}</b> <code>in tmute</code>"
                                           + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                    else:
                        await message.edit(f"<b>{user_to_tmute.first_name}</b> <code>already in tmute</code>")
                        client.add_handler(MessageHandler(restrict_users_in_tmute, filters.group))
                else:
                    await message.edit("<b>Not on yourself</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tunmute"], prefix) & filters.me)
async def tunmute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            if not message.reply_to_message.from_user.is_self:
                find_user = await db.find_one({"USER_ID": f"{message.reply_to_message.from_user.id}",
                                               "CHAT_ID": f"{message.chat.id}"})
                if not find_user:
                    await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>not in tmute</code>")
                else:
                    await db.delete_one(find_user)
                    await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>tunmuted</code>"
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}")
            else:
                await message.edit("<b>Not on yourself</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                user_to_tunmute = await client.get_users(cause.split(" ")[1])
                if not user_to_tunmute.is_self:
                    find_user = await db.find_one({"USER_ID": f"{user_to_tunmute.id}",
                                                   "CHAT_ID": f"{message.chat.id}"})
                    if not find_user:
                        await message.edit(f"<b>{user_to_tunmute.first_name}</b> <code>not in tmute</code>")
                    else:
                        await db.delete_one(find_user)
                        await message.edit(f"<b>{user_to_tunmute.first_name}</b> <code>tunmuted</code>"
                                           + f"\n{'<b>Cause:</b> <i>' + cause.split(maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                else:
                    await message.edit("<b>Not on yourself</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["tmute_users"], prefix) & filters.me)
async def tunmute_users_command(client: Client, message: Message):
    if message.chat.type not in ["private", "channel"]:
        text = f"<b>All users</b> <code>{message.chat.title}</code> <b>who are now in tmute</b>\n\n"
        count = 0
        async for _ in db.find():
            if message.chat.id == int(_["CHAT_ID"]):
                try:
                    _name_ = await client.get_users(_["USER_ID"])
                    count += 1
                    text += f"{count}. <b>{_name_.first_name}</b>\n"
                except PeerIdInvalid:
                    pass
        if count == 0:
            await message.edit("<b>No users in tmute</b>")
        else:
            text += f"\n<b>Total users in tmute</b> {count}"
            await message.edit(text)
    else:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["unmute"], prefix) & filters.me)
async def unmute_command(client, message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        u_p = await chat_permissions(client, message)
        if message.reply_to_message.from_user:
            try:
                await client.restrict_chat_member(message.chat.id,
                                                  message.reply_to_message.from_user.id,
                                                  u_p,
                                                  int(time() + 30))
                await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>unmuted</code>"
                                   + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}")
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
        else:
            await message.edit("<b>Reply on user msg</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        u_p = await chat_permissions(client, message)
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                try:
                    await client.restrict_chat_member(message.chat.id,
                                                      user_to_unmute.id,
                                                      u_p,
                                                      int(time() + 30))
                    await message.edit(f"<b>{user_to_unmute.first_name}</b> <code>unmuted!</code>"
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["mute"], prefix) & filters.me)
async def mute_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        mute_seconds: int = 0
        for character in 'mhdw':
            match = re.search(rf'(\d+|(\d+\.\d+)){character}', message.text)
            if match:
                if character == 'm':
                    mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 60 // 1)
                if character == 'h':
                    mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 3600 // 1)
                if character == 'd':
                    mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 86400 // 1)
                if character == 'w':
                    mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 604800 // 1)
        if mute_seconds > 30:
            try:
                await client.restrict_chat_member(
                       message.chat.id,
                       message.reply_to_message.from_user.id,
                       ChatPermissions(),
                       int(time()) + mute_seconds
                )
                from_user = message.reply_to_message.from_user
                mute_time: Dict[str, int] = {
                    'days': mute_seconds // 86400,
                    'hours': mute_seconds % 86400 // 3600,
                    'minutes': mute_seconds % 86400 % 3600 // 60
                }
                message_text = f"<b>{from_user.first_name}</b> <code> was muted for" \
                               f" {((str(mute_time['days']) + ' day') if mute_time['days'] > 0 else '') + ('s' if mute_time['days'] > 1 else '')}" \
                               f" {((str(mute_time['hours']) + ' hour') if mute_time['hours'] > 0 else '') + ('s' if mute_time['hours'] > 1 else '')}" \
                               f" {((str(mute_time['minutes']) + ' minute') if mute_time['minutes'] > 0 else '') + ('s' if mute_time['minutes'] > 1 else '')}</code>" \
                               + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                while '  ' in message_text:
                    message_text = message_text.replace('  ', ' ')
                await message.edit(message_text)
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
        else:
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    ChatPermissions())
                message_text = f"<b>{message.reply_to_message.from_user.first_name}</b> <code> was muted for never</code>" \
                               + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}"
                await message.edit(message_text)
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                mute_seconds: int = 0
                for character in 'mhdw':
                    match = re.search(rf'(\d+|(\d+\.\d+)){character}', message.text)
                    if match:
                        if character == 'm':
                            mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 60 // 1)
                        if character == 'h':
                            mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 3600 // 1)
                        if character == 'd':
                            mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 86400 // 1)
                        if character == 'w':
                            mute_seconds += int(float(match.string[match.start():match.end() - 1]) * 604800 // 1)
                if mute_seconds > 30:
                    try:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions(),
                            int(time()) + mute_seconds
                        )
                        mute_time: Dict[str, int] = {
                            'days': mute_seconds // 86400,
                            'hours': mute_seconds % 86400 // 3600,
                            'minutes': mute_seconds % 86400 % 3600 // 60
                        }
                        message_text = f"<b>{user_to_unmute.first_name}</b> <code> was muted for" \
                                       f" {((str(mute_time['days']) + ' day') if mute_time['days'] > 0 else '') + ('s' if mute_time['days'] > 1 else '')}" \
                                       f" {((str(mute_time['hours']) + ' hour') if mute_time['hours'] > 0 else '') + ('s' if mute_time['hours'] > 1 else '')}" \
                                       f" {((str(mute_time['minutes']) + ' minute') if mute_time['minutes'] > 0 else '') + ('s' if mute_time['minutes'] > 1 else '')}</code>" \
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=3)[3] + '</i>' if len(cause.split()) > 3 else ''}"
                        while '  ' in message_text:
                            message_text = message_text.replace('  ', ' ')
                        await message.edit(message_text)
                    except UserAdminInvalid:
                        await message.edit("<b>No rights</b>")
                    except ChatAdminRequired:
                        await message.edit("<b>No rights</b>")
                    except Exception as e:
                        print(e)
                        await message.edit("<b>No rights</b>")
                else:
                    try:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions())
                        message_text = f"<b>{user_to_unmute.first_name}</b> <code> was muted for never</code>" \
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}"
                        await message.edit(message_text)
                    except UserAdminInvalid:
                        await message.edit("<b>No rights</b>")
                    except ChatAdminRequired:
                        await message.edit("<b>No rights</b>")
                    except Exception as e:
                        print(e)
                        await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["demote"], prefix) & filters.me)
async def demote_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(message.chat.id,
                                                 message.reply_to_message.from_user.id,
                                                 is_anonymous=False,
                                                 can_manage_chat=False,
                                                 can_change_info=False,
                                                 can_post_messages=False,
                                                 can_edit_messages=False,
                                                 can_delete_messages=False,
                                                 can_restrict_members=False,
                                                 can_invite_users=False,
                                                 can_pin_messages=False,
                                                 can_promote_members=False,
                                                 can_manage_voice_chats=False)
                await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>demoted!</code>"
                                   + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}")
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(message.chat.id,
                                                     promote_user.id,
                                                     is_anonymous=False,
                                                     can_manage_chat=False,
                                                     can_change_info=False,
                                                     can_post_messages=False,
                                                     can_edit_messages=False,
                                                     can_delete_messages=False,
                                                     can_restrict_members=False,
                                                     can_invite_users=False,
                                                     can_pin_messages=False,
                                                     can_promote_members=False,
                                                     can_manage_voice_chats=False)
                    await message.edit(f"<b>{promote_user.first_name}</b> <code>demoted!</code>"
                                       + f"\n{'<b>Cause:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")


@Client.on_message(filters.command(["promote"], prefix) & filters.me)
async def promote_command(client: Client, message: Message):
    cause = await text(client, message)
    if message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(message.chat.id,
                                                 message.reply_to_message.from_user.id,
                                                 can_delete_messages=True,
                                                 can_restrict_members=True,
                                                 can_invite_users=True,
                                                 can_pin_messages=True)
                if len(cause.split()) > 1:
                    await client.set_administrator_title(message.chat.id,
                                                         message.reply_to_message.from_user.id,
                                                         cause.split(maxsplit=1)[1])
                await message.edit(f"<b>{message.reply_to_message.from_user.first_name}</b> <code>promoted!</code>"
                                   + f"\n{'<b>Prefix:</b> <i>' + cause.split(' ', maxsplit=1)[1] + '</i>' if len(cause.split()) > 1 else ''}")
            except UserAdminInvalid:
                await message.edit("<b>No rights</b>")
            except ChatAdminRequired:
                await message.edit("<b>No rights</b>")
            except Exception as e:
                print(e)
                await message.edit("<b>No rights</b>")
    elif not message.reply_to_message \
            and message.chat.type not in ["private", "channel"]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(message.chat.id,
                                                     promote_user.id,
                                                     can_delete_messages=True,
                                                     can_restrict_members=True,
                                                     can_invite_users=True,
                                                     can_pin_messages=True)
                    if len(cause.split()) > 1:
                        await client.set_administrator_title(message.chat.id,
                                                             promote_user.id,
                                                             f"\n{cause.split(' ', maxsplit=2)[2] if len(cause.split()) > 2 else None}")
                    await message.edit(f"<b>{promote_user.first_name}</b> <code>promoted!</code>"
                                       + f"\n{'<b>Prefix:</b> <i>' + cause.split(' ', maxsplit=2)[2] + '</i>' if len(cause.split()) > 2 else ''}")
                except UserAdminInvalid:
                    await message.edit("<b>No rights</b>")
                except ChatAdminRequired:
                    await message.edit("<b>No rights</b>")
                except Exception as e:
                    print(e)
                    await message.edit("<b>No rights</b>")
            except PeerIdInvalid:
                await message.edit("<b>User is not found</b>")
            except UsernameInvalid:
                await message.edit("<b>User is not found</b>")
            except IndexError:
                await message.edit("<b>User is not found</b>")
        else:
            await message.edit("<b>user_id or username</b>")
    elif message.chat.type in ["private", "channel"]:
        await message.edit("<b>Unsupported</b>")

modules_help.update({
                        'admintool': '''ban - reply user message or user_id/username and reason (Available triggers: report_spam and delete_history)
                        , unban - reply user message or user_id/username and reason
                        , kick - reply user message or user_id/username and reason (Available triggers: report_spam and delete_history)
                        , tmute - reply user message or user_id/username and reason
                        , tunmute -  reply user message or user_id/username and reason
                        , tmute_users - cheklist all tmute users
                        , unmute - reply user message or user_id/username and reason
                        , mute - reply user message or user_id/username time in format 1m/1h/1d/1w and reason
                        , promote - reply user message or user_id/username and prefix
                        , demote - reply user message or user_id/username and reason''',
                        'admintool module': 'AdminTool: ban, '
                                         'unban, kick, tmute, tunmute, tmute_users, unmute, mute, promote, demote\n'})