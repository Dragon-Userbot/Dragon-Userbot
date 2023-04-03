import aiohttp
import tempfile

from contextlib import redirect_stdout
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import format_exc

PROXY_SOURCES = {
    "http": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    ],
    "socks4": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    ],
    "socks5": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    ],
    "https": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all",
    ],
}


async def fetch_proxies(session, proxy_type):  # cringe, but why not?
    proxies = []
    for url in PROXY_SOURCES[proxy_type]:
        async with session.get(url) as resp:
            lines = await resp.text()
        for line in lines.split("\n"):
            if not line.strip():
                continue
            parts = line.split(":")
            if len(parts) != 2 and len(parts) != 4:
                continue
            if len(parts) == 4:
                ip, port, _, _ = parts
            else:
                ip, port = parts
            proxy = f"{proxy_type}://{ip}:{port}"
            proxies.append(proxy)

    return proxies


@Client.on_message(filters.command(["pr", "proxys"], prefix) & filters.me)
async def user_exec(client: Client, message: Message):
    proxy_type = "http"
    if len(message.command) > 1:
        proxy_type = message.command[1]

    message = await message.edit("🛡 <b>Parsing...</b>")
    try:
        if proxy_type not in PROXY_SOURCES:
            proxy_types = list(PROXY_SOURCES.keys())
            proxy_types_text = ""
            for i, proxy_type in enumerate(proxy_types):
                proxy_types_text += f"{i+1}. {proxy_type}\n"
            await message.edit(
                "🚫 <b>Invalid proxy type specified.</b>\n\n🪄 <b>Available selection:</b>\n"
                + proxy_types_text
            )
            return

        async with aiohttp.ClientSession() as session:
            proxies = await fetch_proxies(session, proxy_type)

        with tempfile.NamedTemporaryFile(
            mode="w+b", delete=False, suffix=".txt"
        ) as file, redirect_stdout(file):
            for proxy in proxies:
                file.write(proxy.encode("utf-8") + b"\n")
            await message.edit(
                f"✅ <b>{proxy_type.capitalize()} proxies have been parsed. 👇</b>"
            )
            await client.send_document(
                chat_id=message.chat.id,
                document=file.name,
                caption=f"<b>🛡 {proxy_type.capitalize()} Proxies:</b>",
            )

    except Exception as e:
        await message.edit(f"🚫 <b>Error while parsing proxies:</b> {format_exc(e)}")


modules_help["proxy"] = {
    "pr": "Execute proxy parser",
}
