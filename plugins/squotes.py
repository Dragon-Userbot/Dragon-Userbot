import base64
import os
from io import BytesIO
import requests
from pyrogram import Client, filters, errors, types
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command(["q", "quote"], prefix) & filters.me)
async def quote_cmd(client: Client, message: types.Message):
    if not message.reply_to_message:
        return await message.edit("<b>Specify message(s) for quote</b>")

    if len(message.command) > 1 and message.command[1].isdigit():
        count = int(message.command[1])
        if count < 1:
            count = 1
        elif count > 10:
            count = 10
    else:
        count = 1

    is_png = "!png" in message.command or "!file" in message.command
    send_for_me = "!me" in message.command or "!ls" in message.command

    messages = filter(
        lambda x: x.message_id < message.message_id,
        await client.get_messages(
            message.chat.id,
            range(
                message.reply_to_message.message_id,
                message.reply_to_message.message_id + count,
            ),
        ),
    )

    if send_for_me:
        await message.delete()
        message = await client.send_message("me", "<b>Generating...</b>")
    else:
        await message.edit("<b>Generating...</b>")

    url = "https://quotes.fl1yd.su/generate"
    params = {
        "messages": [
            await render_message(client, msg) for msg in messages if not msg.empty
        ],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

    response = requests.post(url, json=params)
    if not response.ok:
        return await message.edit(
            f"<b>Quotes API error!</b>\n" f"<code>{response.text}</code>"
        )

    file_io = BytesIO(response.content)
    if is_png:
        file_io.name = "sticker.png"
    else:
        file_io.name = "sticker.webp"

    await message.edit("<b>Sending...</b>")

    try:
        func = client.send_document if is_png else client.send_sticker
        chat_id = "me" if send_for_me else message.chat.id
        await func(chat_id, file_io)
    except errors.RPCError as e:  # no rights to send stickers, etc
        await message.edit(f"<b>Telegram API error!</b>\n" f"<code>{e}</code>")
    else:
        await message.delete()


@Client.on_message(filters.command(["fq", "fakequote"], prefix) & filters.me)
async def fake_quote_cmd(client: Client, message: types.Message):
    if not message.reply_to_message:
        return await message.edit("<b>Specify message for fake quote</b>")

    is_png = "!png" in message.command or "!file" in message.command
    send_for_me = "!me" in message.command or "!ls" in message.command

    fake_quote_text = " ".join(
        [
            arg
            for arg in message.command[1:]
            if arg not in ["!png", "!file", "!me", "!ls"]
        ]  # remove some special arg words
    )

    if not fake_quote_text:
        return await message.edit("<b>Fake quote text is empty</b>")

    q_message = await client.get_messages(
        message.chat.id, message.reply_to_message.message_id
    )
    q_message.text = fake_quote_text
    q_message.entities = None

    if send_for_me:
        await message.delete()
        message = await client.send_message("me", "<b>Generating...</b>")
    else:
        await message.edit("<b>Generating...</b>")

    url = "https://quotes.fl1yd.su/generate"
    params = {
        "messages": [await render_message(client, q_message)],
        "quote_color": "#162330",
        "text_color": "#fff",
    }

    response = requests.post(url, json=params)
    if not response.ok:
        return await message.edit(
            f"<b>Quotes API error!</b>\n" f"<code>{response.text}</code>"
        )

    file_io = BytesIO(response.content)
    if is_png:
        file_io.name = "sticker.png"
    else:
        file_io.name = "sticker.webp"

    await message.edit("<b>Sending...</b>")

    try:
        func = client.send_document if is_png else client.send_sticker
        chat_id = "me" if send_for_me else message.chat.id
        await func(chat_id, file_io)
    except errors.RPCError as e:  # no rights to send stickers, etc
        await message.edit(f"<b>Telegram API error!</b>\n" f"<code>{e}</code>")
    else:
        await message.delete()


async def render_message(app: Client, message: types.Message) -> dict:
    async def get_file(file_id) -> str:
        file_name = await app.download_media(file_id)
        with open(file_name, "rb") as f:
            content = f.read()
        os.remove(file_name)
        data = base64.b64encode(content).decode()
        return data

    # text
    if message.photo:
        text = message.caption if message.caption else ""
    elif message.poll:
        text = get_poll_text(message.poll)
    elif message.sticker:
        text = ""
    else:
        text = get_reply_text(message)

    # media
    if message.photo:
        media = await get_file(message.photo.file_id)
    elif message.sticker:
        media = await get_file(message.sticker.file_id)
    else:
        media = ""

    # entities
    entities = []
    if message.entities:
        for entity in message.entities:
            entities.append(
                {
                    "offset": entity.offset,
                    "length": entity.length,
                    "type": entity.type,
                }
            )

    def move_forwards(msg: types.Message):
        if msg.forward_from:
            msg.from_user = msg.forward_from
        elif msg.forward_sender_name:
            msg.from_user.id = 0
            msg.from_user.first_name = msg.forward_sender_name
            msg.from_user.last_name = ""
        elif msg.forward_from_chat:
            msg.sender_chat = msg.forward_from_chat

    move_forwards(message)

    # author
    author = {}
    if message.from_user:
        author["id"] = message.from_user.id
        author["name"] = get_full_name(message.from_user)
        if message.chat.type != "supergroup" or message.from_user.id == 0:
            author["rank"] = ""
        else:
            try:
                member = await message.chat.get_member(message.from_user.id)
            except errors.UserNotParticipant:
                author["rank"] = ""
            else:
                author["rank"] = getattr(member, "title", "") or (
                    "owner"
                    if member.status == "creator"
                    else "admin"
                    if member.status == "administrator"
                    else ""
                )

        if message.from_user.id == 0 or not message.from_user.photo:
            author["avatar"] = ""
        else:
            author["avatar"] = await get_file(message.from_user.photo.big_file_id)
    else:
        author["id"] = message.sender_chat.id
        author["name"] = message.sender_chat.title
        author["rank"] = "channel" if message.sender_chat.type == "channel" else ""

        if message.sender_chat.photo:
            author["avatar"] = await get_file(message.sender_chat.photo.big_file_id)
        else:
            author["avatar"] = ""
    author["via_bot"] = message.via_bot.username if message.via_bot else ""

    # reply
    reply = {}
    reply_msg = message.reply_to_message
    if reply_msg and not reply_msg.empty:
        move_forwards(reply_msg)

        if reply_msg.from_user:
            reply["id"] = reply_msg.from_user.id
            reply["name"] = get_full_name(reply_msg.from_user)
        else:
            reply["id"] = reply_msg.sender_chat.id
            reply["name"] = reply_msg.sender_chat.title

        reply["text"] = get_reply_text(reply_msg)

    return {
        "text": text,
        "media": media,
        "entities": entities,
        "author": author,
        "reply": reply,
    }


def get_audio_text(audio: types.Audio) -> str:
    if audio.title and audio.performer:
        return f" ({audio.title} — {audio.performer})"
    elif audio.title:
        return f" ({audio.title})"
    elif audio.performer:
        return f" ({audio.performer})"
    else:
        return ""


def get_reply_text(reply: types.Message) -> str:
    text = (
        "📷 Photo" + ("\n" + reply.caption if reply.caption else "")
        if reply.photo
        else get_reply_poll_text(reply.poll)
        if reply.poll
        else "📍 Location"
        if reply.location or reply.venue
        else "👤 Contact"
        if reply.contact
        else "🖼 GIF"
        if reply.animation
        else "🎧 Music" + get_audio_text(reply.audio)
        if reply.audio
        else "📹 Video"
        if reply.video
        else "📹 Videomessage"
        if reply.video_note
        else "🎵 Voice"
        if reply.voice
        else (reply.sticker.emoji + " " if reply.sticker.emoji else "") + "Sticker"
        if reply.sticker
        else "💾 File " + reply.document.file_name
        if reply.document
        else "🎮 Game"
        if reply.game
        else "🎮 set new record"
        if reply.game_high_score
        else f"{reply.dice.emoji} - {reply.dice.value}"
        if reply.dice
        else (
            "👤 joined the group"
            if reply.new_chat_members[0].id == reply.from_user.id
            else "👤 invited %s to the group"
            % (get_full_name(reply.new_chat_members[0]))
        )
        if reply.new_chat_members
        else (
            "👤 left the group"
            if reply.left_chat_member.id == reply.from_user.id
            else "👤 removed %s" % (get_full_name(reply.left_chat_member))
        )
        if reply.left_chat_member
        else f"✏ changed group name to {reply.new_chat_title}"
        if reply.new_chat_title
        else "🖼 changed group photo"
        if reply.new_chat_photo
        else "🖼 removed group photo"
        if reply.delete_chat_photo
        else "📍 pinned message"
        if reply.pinned_message
        else "🎤 started a new video chat"
        if reply.voice_chat_started
        else "🎤 ended the video chat"
        if reply.voice_chat_ended
        else "🎤 invited participants to the video chat"
        if reply.voice_chat_members_invited
        else "👥 created the group"
        if reply.group_chat_created or reply.supergroup_chat_created
        else "👥 created the channel"
        if reply.channel_chat_created
        else reply.text or "unsupported message"
    )

    return text


def get_poll_text(poll: types.Poll) -> str:
    text = get_reply_poll_text(poll) + "\n"

    text += poll.question + "\n"
    for option in poll.options:
        text += f"- {option.text}"
        if option.voter_count > 0:
            text += f" ({option.voter_count} voted)"
        text += "\n"

    text += f"Total: {poll.total_voter_count} voted"

    return text


def get_reply_poll_text(poll: types.Poll) -> str:
    if poll.is_anonymous:
        if poll.type == "regular":
            text = "📊 Anonymous poll"
        else:
            text = "📊 Anonymous quiz"
    else:
        if poll.type == "regular":
            text = "📊 Poll"
        else:
            text = "📊 Quiz"

    if poll.is_closed:
        text += " (closed)"

    return text


def get_full_name(user: types.User) -> str:
    name = user.first_name
    if user.last_name:
        name += " " + user.last_name
    return name


modules_help.append(
    {
        "squotes": [
            {
                "q [reply]* [count] [args]": "Generate a quote\nAvailable args: !png — send quote as png; !me — send quote to saved messages"
            },
            {"fq [text]* [userid]/[reply]* [args] [text]": "Generate a fake quote"},
        ]
    }
)
