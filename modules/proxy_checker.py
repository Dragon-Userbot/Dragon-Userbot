# Description: The module to check the validity of a single proxy
import aiohttp

from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import format_exc

async def check_proxy(proxy: str): 
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.google.com", proxy=proxy, timeout=5) as resp:
                return resp.status == 200
    except Exception:
        return False

@Client.on_message(filters.command(["check_proxy", "chk"], prefix) & filters.me)
async def check_proxy_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit("🚫 <b>Please specify a proxy to check.</b>\n\n👉 <b>An example:</b> <code>socks4://1337:228</code>")
        return

    proxy = message.command[1]
    message = await message.edit(f"🛡 <b>Checking proxy</b> <code>{proxy}</code>...")

    if not await check_proxy(proxy):
        await message.edit(f"❌ <b>Proxy</b> <code>{proxy}</code> is invalid.")
    else:
        await message.edit(f"✅ <b>Proxy</b> <code>{proxy}</code> is valid.")

modules_help["check_proxy"] = {
    "check_proxy": "The module to check the validity of a single proxy",
}
