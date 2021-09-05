from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix, sessionkiller_enabled, config_path, config
from .utils.scripts import restart
from pyrogram.raw.functions.account import GetAuthorizations, ResetAuthorization
from pyrogram.raw.types import UpdateServiceNotification
from html import escape
from datetime import datetime
import time

@Client.on_message(filters.command(['sessionkiller', 'sk'], prefix) & filters.me)
async def sessionkiller(client: Client, message: Message):
    if len(message.command) == 1:
        if sessionkiller_enabled:
            await message.edit('Sessionkiller status: <b>enabled</b>\n'
                               f'You can disable it with <code>{prefix}sessionkiller disable</code>')
        else:
            await message.edit('Sessionkiller status: <b>disabled</b>\n'
                               f'You can enable it with <code>{prefix}sessionkiller enable</code>')
    else:
        if message.command[1] in ['enable', 'on', '1', 'yes']:
            config.set('sessionkiller', 'enabled', '1')
            with open(config_path, "w") as config_file:
                config.write(config_file)
            await message.edit(f'<b>Sessionkiller enabled!</b>')
            await restart()
        elif message.command[1] in ['disable', 'off', '0', 'no']:
            config.set('sessionkiller', 'enabled', '0')
            with open(config_path, "w") as config_file:
                config.write(config_file)
            await message.edit(f'<b>Sessionkiller disabled!</b>')
            await restart()
        else:
            await message.edit(f'<b>Usage: {prefix}sessionkiller [enable|disable]</b>')


@Client.on_raw_update()
async def check_new_login(client: Client, update: UpdateServiceNotification, _, __):
    if not sessionkiller_enabled:
        return
    if not isinstance(update, UpdateServiceNotification) or \
            not update.type.startswith('auth'):
        return
    authorizations = (await client.send(GetAuthorizations()))['authorizations']
    for auth in authorizations:
        if auth.current:
            continue
        if (time.time() - auth.date_created) < 3:
            # found new unexpected login
            try:
                await client.send(ResetAuthorization(hash=auth.hash))
            except:
                info_text = "Someone tried to log in to your account. You can see this report because " \
                            "turned on this feature. But I couldn't terminate attacker's session and " \
                            "⚠ <b>you must reset it manually</b>. You should change your 2FA password " \
                            "(if enabled), or setup it.\n"
            else:
                info_text = "Someone tried to log in to your account. Since you have enabled " \
                            "this feature, we have deleted the attacker's session from this account. " \
                            "You should change your 2FA password (if enabled), or setup it.\n"
            logined_time = datetime.utcfromtimestamp(auth.date_created).strftime('%d-%m-%Y %H-%M-%S UTC')
            data = '<b>!!! ACTION REQUIRED !!!</b>\n' \
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
                   f'<b>It is you? Type <code>{prefix}sessionkiller disable</code> and try logging ' \
                   f'in again.</b>'
            me = await client.get_me()
            await client.send_message(me.id, data)  # sending report to saved messages
            return


modules_help.update(
    {'sessionkiller': '''sessionkiller [enable|disable] - When enabled，every new session will be terminated]
[Useful for additional protection for your account''',
     'sessionkiller module': 'Sessionkiller: sessionkiller</code> or <code>sk',
     'sk': 'sk [on|off] - see sessionkiller help (all commands are exactly same)'})

