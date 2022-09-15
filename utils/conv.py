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
from collections import OrderedDict

from pyrogram import Client, filters, types
from pyrogram.handlers import MessageHandler

import asyncio
from typing import Union, List, Dict, Optional


class _TrueFilter(filters.Filter):
    async def __call__(self, client: Client, update: types.Message):
        return True


class Conversation:
    _locks: Dict[int, asyncio.Lock] = {}

    def __init__(
        self,
        client: Client,
        chat: Union[str, int],
        timeout: float = 5,
        delete_at_end=True,
        exclusive=True,
    ):
        self.client = client
        self.chat = chat
        self.timeout = timeout
        self.delete_at_end = delete_at_end
        self.exclusive = exclusive

        self._chat_id = 0
        self._message_ids = []
        self._handler_object = None
        self._chat_unique_lock: Optional[asyncio.Lock] = None
        self._waiters: Dict[asyncio.Event, filters.Filter] = {}
        self._responses: Dict[asyncio.Event, types.Message] = {}
        self._pending_updates: List[types.Message] = []

    async def __aenter__(self):
        self._chat_id = (await self.client.get_chat(self.chat)).id

        if self._chat_id in self._locks:
            self._chat_unique_lock = self._locks[self._chat_id]
        else:
            self._chat_unique_lock = self._locks[self._chat_id] = asyncio.Lock()

        if self.exclusive:
            await self._chat_unique_lock.acquire()

        self._handler_object = MessageHandler(
            self._handler, filters.chat(self._chat_id)
        )

        if -999 not in self.client.dispatcher.groups:
            self.client.dispatcher.groups[-999] = []
            self.client.dispatcher.groups = OrderedDict(
                sorted(self.client.dispatcher.groups.items())
            )

        self.client.dispatcher.groups[-999].append(self._handler_object)

        await asyncio.sleep(0)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.dispatcher.groups[-999].remove(self._handler_object)

        if self.delete_at_end:
            await self.client.delete_messages(self._chat_id, self._message_ids)

        if self.exclusive:
            self._chat_unique_lock.release()

    async def _handler(self, _, message: types.Message):
        for event, message_filter in self._waiters.items():
            if await message_filter(self.client, message):
                self._responses[event] = message
                event.set()
                break
        else:
            self._pending_updates.append(message)
        message.continue_propagation()

    async def get_response(
        self,
        message_filter: Optional[filters.Filter] = None,
        timeout: float = None,
    ) -> types.Message:
        if timeout is None:
            timeout = self.timeout
        if message_filter is None:
            message_filter = _TrueFilter()

        for message in self._pending_updates:
            if await message_filter(self.client, message):
                self._pending_updates.remove(message)
                break
        else:
            message = await self._wait_message(message_filter, timeout)

        self._message_ids.append(message.id)
        return message

    async def _wait_message(
        self, message_filter: Optional[filters.Filter], timeout: float
    ) -> types.Message:
        event = asyncio.Event()
        self._waiters[event] = message_filter

        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
        except asyncio.TimeoutError as e:
            raise TimeoutError from e
        finally:
            self._waiters.pop(event)

        return self._responses.pop(event)

    async def send_message(
        self,
        text: str,
        parse_mode: Optional[str] = object,
        entities: List[types.MessageEntity] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
    ) -> types.Message:
        """Send text messages.

        Parameters:
            text (``str``):
                Text of the message to be sent.

            parse_mode (``str``, *optional*):
                By default, texts are parsed using HTML style.
                Pass "markdown" or "md" to enable Markdown-style parsing.
                Pass None to completely disable style parsing.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (``int``, *optional*):
                Date when the message will be automatically sent. Unix time.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent text message is returned.
        """

        sent = await self.client.send_message(
            chat_id=self._chat_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            schedule_date=schedule_date,
        )
        self._message_ids.append(sent.id)
        return sent
