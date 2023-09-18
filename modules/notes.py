#  Dragon-Userbot - telegram userbot
#  Copyright (C) 2020-present Dragon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pyrogram import Client, filters, errors
from pyrogram.types import (
    Message,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAudio,
    InputMediaDocument,
)

from utils.db import db
from utils.misc import modules_help, prefix

#  from utils.scripts import with_reply


@Client.on_message(filters.command(["save"], prefix) & filters.me)
async def save_note(client: Client, message: Message):
    await message.edit("<b>Loading...</b>")

    try:
        chat = await client.get_chat(db.get("core.notes", "chat_id", 0))
    except (errors.RPCError, ValueError, KeyError):
        # group is not accessible or isn't created
        chat = await client.create_supergroup(
            "Dragon_Userbot_Notes_Filters", "Don't touch this group, please"
        )
        db.set("core.notes", "chat_id", chat.id)

    chat_id = chat.id

    if message.reply_to_message and len(message.text.split()) >= 2:
        note_name = message.text.split(maxsplit=1)[1]
        if message.reply_to_message.media_group_id:
            checking_note = db.get("core.notes", f"note{note_name}", False)
            if not checking_note:
                get_media_group = [
                    _.id
                    for _ in await client.get_media_group(
                        message.chat.id, message.reply_to_message.id
                    )
                ]
                try:
                    message_id = await client.forward_messages(
                        chat_id, message.chat.id, get_media_group
                    )
                except errors.ChatForwardsRestricted:
                    await message.edit(
                        "<b>Forwarding messages is restricted by chat admins</b>"
                    )
                    return
                note = {
                    "MESSAGE_ID": str(message_id[1].id),
                    "MEDIA_GROUP": True,
                    "CHAT_ID": str(chat_id),
                }
                db.set("core.notes", f"note{note_name}", note)
                await message.edit(f"<b>Note {note_name} saved</b>")
            else:
                await message.edit("<b>This note already exists</b>")
        else:
            checking_note = db.get("core.notes", f"note{note_name}", False)
            if not checking_note:
                try:
                    message_id = await message.reply_to_message.forward(chat_id)
                except errors.ChatForwardsRestricted:
                    message_id = await message.copy(chat_id)
                note = {
                    "MEDIA_GROUP": False,
                    "MESSAGE_ID": str(message_id.id),
                    "CHAT_ID": str(chat_id),
                }
                db.set("core.notes", f"note{note_name}", note)
                await message.edit(f"<b>Note {note_name} saved</b>")
            else:
                await message.edit("<b>This note already exists</b>")
    elif len(message.text.split()) >= 3:
        note_name = message.text.split(maxsplit=1)[1].split()[0]
        checking_note = db.get("core.notes", f"note{note_name}", False)
        if not checking_note:
            message_id = await client.send_message(
                chat_id, message.text.split(note_name)[1].strip()
            )
            note = {
                "MEDIA_GROUP": False,
                "MESSAGE_ID": str(message_id.id),
                "CHAT_ID": str(chat_id),
            }
            db.set("core.notes", f"note{note_name}", note)
            await message.edit(f"<b>Note {note_name} saved</b>")
        else:
            await message.edit("<b>This note already exists</b>")
    else:
        await message.edit(
            f"<b>Example: <code>{prefix}save note_name</code></b>"
        )


@Client.on_message(filters.command(["note"], prefix) & filters.me)
async def note_send(client: Client, message: Message):
    if len(message.text.split()) >= 2:
        await message.edit("<b>Loading...</b>")

        note_name = f"{message.text.split(maxsplit=1)[1]}"
        find_note = db.get("core.notes", f"note{note_name}", False)
        if find_note:
            try:
                await client.get_messages(
                    int(find_note["CHAT_ID"]), int(find_note["MESSAGE_ID"])
                )
            except errors.RPCError:
                await message.edit(
                    "<b>Sorry, but this note is unavaliable.\n\n"
                    f"You can delete this note with "
                    f"<code>{prefix}clear {note_name}</code></b>"
                )
                return

            if find_note.get("MEDIA_GROUP"):
                messages_grouped = await client.get_media_group(
                    int(find_note["CHAT_ID"]), int(find_note["MESSAGE_ID"])
                )
                media_grouped_list = []
                for _ in messages_grouped:
                    if _.photo:
                        if _.caption:
                            media_grouped_list.append(
                                InputMediaPhoto(
                                    _.photo.file_id, _.caption.markdown
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaPhoto(_.photo.file_id)
                            )
                    elif _.video:
                        if _.caption:
                            if _.video.thumbs:
                                media_grouped_list.append(
                                    InputMediaVideo(
                                        _.video.file_id,
                                        _.video.thumbs[0].file_id,
                                        _.caption.markdown,
                                    )
                                )
                            else:
                                media_grouped_list.append(
                                    InputMediaVideo(
                                        _.video.file_id, _.caption.markdown
                                    )
                                )
                        elif _.video.thumbs:
                            media_grouped_list.append(
                                InputMediaVideo(
                                    _.video.file_id, _.video.thumbs[0].file_id
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaVideo(_.video.file_id)
                            )
                    elif _.audio:
                        if _.caption:
                            media_grouped_list.append(
                                InputMediaAudio(
                                    _.audio.file_id, _.caption.markdown
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaAudio(_.audio.file_id)
                            )
                    elif _.document:
                        if _.caption:
                            if _.document.thumbs:
                                media_grouped_list.append(
                                    InputMediaDocument(
                                        _.document.file_id,
                                        _.document.thumbs[0].file_id,
                                        _.caption.markdown,
                                    )
                                )
                            else:
                                media_grouped_list.append(
                                    InputMediaDocument(
                                        _.document.file_id, _.caption.markdown
                                    )
                                )
                        elif _.document.thumbs:
                            media_grouped_list.append(
                                InputMediaDocument(
                                    _.document.file_id,
                                    _.document.thumbs[0].file_id,
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaDocument(_.document.file_id)
                            )
                if message.reply_to_message:
                    await client.send_media_group(
                        message.chat.id,
                        media_grouped_list,
                        reply_to_message_id=message.reply_to_message.id,
                    )
                else:
                    await client.send_media_group(
                        message.chat.id, media_grouped_list
                    )
            elif message.reply_to_message:
                await client.copy_message(
                    message.chat.id,
                    int(find_note["CHAT_ID"]),
                    int(find_note["MESSAGE_ID"]),
                    reply_to_message_id=message.reply_to_message.id,
                )
            else:
                await client.copy_message(
                    message.chat.id,
                    int(find_note["CHAT_ID"]),
                    int(find_note["MESSAGE_ID"]),
                )
            await message.delete()
        else:
            await message.edit("<b>There is no such note</b>")
    else:
        await message.edit(
            f"<b>Example: <code>{prefix}note note_name</code></b>"
        )


@Client.on_message(filters.command(["notes"], prefix) & filters.me)
async def notes(_, message: Message):
    await message.edit("<b>Loading...</b>")
    text = "Available notes:\n\n"
    collection = db.get_collection("core.notes")
    for note in collection.keys():
        if note[:4] == "note":
            text += f"<code>{note[4:]}</code>\n"
    await message.edit(text)


@Client.on_message(filters.command(["clear"], prefix) & filters.me)
async def clear_note(_, message: Message):
    if len(message.text.split()) >= 2:
        note_name = message.text.split(maxsplit=1)[1]
        find_note = db.get("core.notes", f"note{note_name}", False)
        if find_note:
            db.remove("core.notes", f"note{note_name}")
            await message.edit(f"<b>Note {note_name} deleted</b>")
        else:
            await message.edit("<b>There is no such note</b>")
    else:
        await message.edit(
            f"<b>Example: <code>{prefix}clear note_name</code></b>"
        )


modules_help["notes"] = {
    "save [name]*": "Save note",
    "note [name]*": "Get saved note",
    "notes": "Get note list",
    "clear [name]*": "Delete note",
}
