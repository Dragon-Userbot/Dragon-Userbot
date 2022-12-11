import asyncio
from datetime import datetime, timedelta
from html import escape as t

from glQiwiApi import QiwiP2PClient
from pyrogram import Client, filters, types

from utils.db import db
from utils.misc import modules_help, prefix


@Client.on_message(filters.command("qiwi", prefix) & filters.me)
async def qiwi(client: Client, message: types.Message):
    if len(message.text.split()) != 3:
        await message.edit(
            f"<b>Invalid command usage!</b>\n\nUse <code>{config.userbot.prefix}qiwi [amount] [expire]</code> instead.\n\nOld message: <code>{t(message.text)}</code>")
        return
    if db.get(
            'core.qiwi',
            'token',
            {
                'token': None
            }
    )['token'] is None:
        await message.edit(
            f"<b>Need qiwi p2p token</b>\n\nUse <code>{prefix}qiwist [token]</code> to add token.")
        return
    await message.edit("<b>Starting to generate an invoice...</b>")
    amount, expire = message.text.split()[1:]
    try:
        async with QiwiP2PClient(secret_p2p=db.get('core.qiwi', 'token', {'token': None})['token']) as p2p:
            invoice = await p2p.create_p2p_bill(amount=amount,
                                                expire_at=datetime.now() + timedelta(minutes=int(expire)))
            await message.edit(
                f"<b>Invoice successfully generated!</b>\n\n<b>Amount:</b> <code>{invoice.amount.value} {invoice.amount.currency}</code>\n"
                f"<b>Expire:</b> <code>{invoice.expire_at}</code>\n<b>Invoice ID:</b> <code>{invoice.id}</code>\n"
                f"<b>Invoice URL:</b> {invoice.pay_url}")
            client.loop.create_task(check_invoice(client, message, invoice.id))
    except Exception as e:
        await message.edit(
            f"<b>Something went wrong!</b>\n<code>{t(str(e))}</code>\n\nOld message: <code>{t(message.text)}</code>")
        return


async def check_invoice(client: Client, message: types.Message, invoice_id: str):
    token = db.get('core.qiwi', 'token', {'token': None})['token']
    async with QiwiP2PClient(secret_p2p=token) as p2p:
        bill_status = await p2p.get_bill_status(bill_id=invoice_id)
        while bill_status != 'PAID' and bill_status != 'EXPIRED':
            await asyncio.sleep(10)
            bill_status = await p2p.get_bill_status(bill_id=invoice_id)
        if await p2p.get_bill_status(invoice_id) == 'PAID':
            await client.send_message(message.chat.id, f'<b>Invoice {invoice_id} successfully paid!</b>')


@Client.on_message(filters.command("qiwist", prefix) & filters.me)
async def qiwist(client: Client, message: types.Message):
    if len(message.command) == 1:
        await message.edit(
            f"<b>Invalid command usage!</b>\n\nUse <code>{prefix}qiwist [token]</code> instead.")
        return
    db.set(
        'core.qiwi',
        'token',
        {
            'token': message.command[1]
        }
    )
    await message.edit(f"<b>Successfully added qiwi p2p token!</b>")


modules_help['Qiwi pay'] = {
    f'<code>qiwi [amount] [expire]</code>': 'Generate qiwi invoice',
}
modules_help['Qiwi Add Token'] = {
    f'<code>qiwist [token]</code>': 'Add or update qiwi p2p token',
}
