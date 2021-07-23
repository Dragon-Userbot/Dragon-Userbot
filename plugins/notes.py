from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
from .utils.utils import createDB, modules_help, prefix

db = createDB.notes


@Client.on_message(filters.command(["save"], prefix) & filters.me)
async def save_note(client: Client, message: Message):
    await message.edit("<code>Loading...</code>")
    async def chat_id():
        cheking_chat_id = await db.find_one({"SAVED": "YES"})
        if cheking_chat_id:
            return cheking_chat_id["CHAT_ID"]
        else:
            chat = await client.create_supergroup(f"Dragon_Userbot_Notes_Filters",
                                                  "Don't")
            save_chat_id = {"SAVED": "YES",
                            "CHAT_ID": f"{chat.id}"}
            await db.insert_one(save_chat_id)
            return chat.id
    if message.reply_to_message and len(message.text.split()) >= 2:
        if message.reply_to_message.media_group_id:
            cheking_note = await db.find_one({"NAME": f"{message.text.split(' ', maxsplit=1)[1]}"})
            if not cheking_note:
                get_media_group = [_.message_id for _ in await client.get_media_group(message.chat.id,
                                                                                            message.reply_to_message.message_id)]
                message_id = await client.forward_messages(await chat_id(),
                                              message.chat.id,
                                              get_media_group)
                note = {"NAME": f"{message.text.split(' ', maxsplit=1)[1]}",
                        "MESSAGE_ID": f"{message_id[1].message_id}",
                        "MEDIA_GROUP_ID": "YES",
                        "CHAT_ID": f"{await chat_id()}"}
                await db.insert_one(note)
                await message.edit(f"Note {message.text.split(' ', maxsplit=1)[1]} saved")
            else:
                await message.edit("This note already exists")
        else:
            cheking_note = await db.find_one({"NAME": f"{message.text.split(' ', maxsplit=1)[1]}"})
            if not cheking_note:
                message_id = await message.reply_to_message.forward(await chat_id())
                note = {"NAME": f"{message.text.split(' ', maxsplit=1)[1]}",
                        "MESSAGE_ID": f"{message_id.message_id}",
                        "CHAT_ID": f"{await chat_id()}"}
                await db.insert_one(note)
                await message.edit(f"Note {message.text.split(' ', maxsplit=1)[1]} saved")
            else:
                await message.edit("This note already exists")
    else:
        await message.edit(f"Example: <code>{prefix}save name note</code> Reply on user message")


@Client.on_message(filters.command(["note"], prefix) & filters.me)
async def note_send(client: Client, message: Message):
    await message.edit("<code>Loading...</code>")
    if len(message.text.split()) >= 2:
        find_note = await db.find_one({"NAME": f"{message.text.split(' ', maxsplit=1)[1]}"})
        if find_note:
            if "MEDIA_GROUP_ID" in find_note:
                messages_grouped = await client.get_media_group(int(find_note["CHAT_ID"]), int(find_note["MESSAGE_ID"]))
                media_grouped_list = []
                for _ in messages_grouped:
                    if _.photo:
                        if _.caption:
                            media_grouped_list.append(InputMediaPhoto(_.photo.file_id,
                                                                      _.caption.markdown))
                        else:
                            media_grouped_list.append(InputMediaPhoto(_.photo.file_id))
                    elif _.video:
                        if _.caption:
                            if _.video.thumbs:
                                media_grouped_list.append(InputMediaVideo(_.video.file_id,
                                                                          _.video.thumbs[0].file_id,
                                                                          _.caption.markdown))
                            else:
                                media_grouped_list.append(InputMediaVideo(_.video.file_id,
                                                                          _.caption.markdown))
                        else:
                            if _.video.thumbs:
                                media_grouped_list.append(InputMediaVideo(_.video.file_id,
                                                                          _.video.thumbs[0].file_id))
                            else:
                                media_grouped_list.append(InputMediaVideo(_.video.file_id))
                    elif _.audio:
                        if _.caption:
                            media_grouped_list.append(InputMediaAudio(_.audio.file_id,
                                                                      _.caption.markdown))
                        else:
                            media_grouped_list.append(InputMediaAudio(_.audio.file_id))
                    elif _.document:
                        if _.caption:
                            if _.document.thumbs:
                                media_grouped_list.append(InputMediaDocument(_.document.file_id,
                                                                             _.document.thumbs[0].file_id,
                                                                             _.caption.markdown))
                            else:
                                media_grouped_list.append(InputMediaDocument(_.document.file_id,
                                                                             _.caption.markdown))
                        else:
                            if _.document.thumbs:
                                media_grouped_list.append(InputMediaDocument(_.document.file_id,
                                                                             _.document.thumbs[0].file_id))
                            else:
                                media_grouped_list.append(InputMediaDocument(_.document.file_id))
                if message.reply_to_message:
                    await client.send_media_group(message.chat.id,
                                                  media_grouped_list,
                                                  reply_to_message_id=message.reply_to_message.message_id)
                else:
                    await client.send_media_group(message.chat.id,
                                                  media_grouped_list)
                await message.delete()
            else:
                if message.reply_to_message:
                    await client.copy_message(message.chat.id,
                                              int(find_note["CHAT_ID"]),
                                              int(find_note["MESSAGE_ID"]),
                                              reply_to_message_id=message.reply_to_message.message_id)
                else:
                    await client.copy_message(message.chat.id,
                                              int(find_note["CHAT_ID"]),
                                              int(find_note["MESSAGE_ID"]))
                await message.delete()
        else:
            await message.edit("There is no such note")
    else:
        await message.edit(f"Example: <code>{prefix}note name note</code>")


@Client.on_message(filters.command(["notes"], prefix) & filters.me)
async def notes(client: Client, message: Message):
    await message.edit("<code>Loading...</code>")
    text = "Available notes\n\n"
    async for _ in db.find():
        if "NAME" in _:
            text += f"<code>{_['NAME']}</code>\n"
    await message.edit(text)


@Client.on_message(filters.command(["clear"], prefix) & filters.me)
async def clear_note(client: Client, message: Message):
    await message.edit("<code>Loading...</code>")
    if len(message.text.split()) >= 2:
        find_note = await db.find_one({"NAME": f"{message.text.split(' ', maxsplit=1)[1]}"})
        if find_note:
            await db.delete_one({"NAME": f"{message.text.split(' ', maxsplit=1)[1]}"})
            await message.edit(f"Note {message.text.split(' ', maxsplit=1)[1]} deleted")
        else:
            await message.edit("There is no such note")
    else:
        await message.edit(f"Example: <code>{prefix}clear name note</code>")



modules_help.update({'notes': '''save |name note| - Reply on user message, note |name note| - Cheking note, notes - Cheking notes, clear - Delete note''',
'notes module': 'Notes: save, '
                'note, notes, clear\n'})
