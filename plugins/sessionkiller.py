from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import Message
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from pyrogram.raw.types import UpdateServiceNotification
from pyrogram import ContinuePropagation
from .utils.utils import modules_help, prefix
from .utils.db import db
from html import escape
from datetime import datetime
from main import app
import asyncio
import time

auth_hashes = db.get('core.sessionkiller', 'auths_hashes', [])

@Client.on_message(filters.command(['sessionkiller', 'sk'], prefix) & filters.me)
async def sessionkiller(_, message: Message):
    if len(message.command) == 1:
        if db.get('core.sessionkiller', 'enabled', False):
            await message.edit('Sessionkiller status: <b>enabled</b>\n'
                               f'You can disable it with <code>{prefix}sessionkiller disable</code>')
        else:
            await message.edit('Sessionkiller status: <b>disabled</b>\n'
                               f'You can enable it with <code>{prefix}sessionkiller enable</code>')
    else:
        if message.command[1] in ['enable', 'on', '1', 'yes', 'true']:
            db.set('core.sessionkiller', 'enabled', True)
            await message.edit(f'<b>Sessionkiller enabled!</b>')
        elif message.command[1] in ['disable', 'off', '0', 'no', 'false']:
            db.set('core.sessionkiller', 'enabled', False)
            await message.edit(f'<b>Sessionkiller disabled!</b>')
        else:
            await message.edit(f'<b>Usage: {prefix}sessionkiller [enable|disable]</b>')


@Client.on_raw_update()
async def check_new_login(client: Client, update: UpdateServiceNotification, _, __):
    if not isinstance(update, UpdateServiceNotification) or \
            not update.type.startswith('auth'):
        raise ContinuePropagation
    if not db.get('core.sessionkiller', 'enabled', False):
        raise ContinuePropagation
    authorizations = (await client.send(GetAuthorizations()))['authorizations']
    for auth in authorizations:
        if auth.current:
            continue
        if auth['hash'] not in auth_hashes:
            # found new unexpected login
            try:
                await client.send(ResetAuthorization(hash=auth.hash))
            except RPCError:
                info_text = "Someone tried to log in to your account. You can see this report because you" \
                            "turned on this feature. But I couldn't terminate attacker's session and " \
                            "⚠ <b>you must reset it manually</b>. You should change your 2FA password " \
                            "(if enabled), or set it.\n"
            else:
                info_text = "Someone tried to log in to your account. Since you have enabled " \
                            "this feature, I deleted the attacker's session from your account. " \
                            "You should change your 2FA password (if enabled), or set it.\n"
            logined_time = datetime.utcfromtimestamp(auth.date_created).strftime('%d-%m-%Y %H-%M-%S UTC')
            full_report = '<b>!!! ACTION REQUIRED !!!</b>\n' \
                          + info_text + \
                          "Below is the information about the attacker that I got.\n\n" \
                          f'Unique authorization hash: <code>{auth.hash}</code> (not valid anymore)\n' \
                          f'Device model: <code>{escape(auth.device_model)}</code>\n' \
                          f'Platform: <code>{escape(auth.platform)}</code>\n' \
                          f'API ID: <code>{auth.api_id}</code>\n' \
                          f'App name: <code>{escape(auth.app_name)}</code>\n' \
                          f'App version: <code>{auth.app_version}</code>\n' \
                          f'Logined at: <code>{logined_time}</code>\n' \
                          f'IP: <code>{auth.ip}</code>\n' \
                          f'Country: <code>{auth.country}</code>\n' \
                          f'Official app: <b>{"yes" if auth.official_app else "no"}</b>\n\n' \
                          f'<b>It is you? Type <code>{prefix}sk off</code> and try logging ' \
                          f'in again.</b>'
            # schedule sending report message so user will get notification
            schedule_date = int(time.time() + 5)
            await client.send_message('me', full_report, schedule_date=schedule_date)
            return


modules_help.update(
    {'sessionkiller': '''sessionkiller [enable|disable] - When enabled，every new session will be terminated.] 
[Useful for additional protection for your account''',
     'sessionkiller module': 'Sessionkiller: sessionkiller</code> or <code>sk',
     })
