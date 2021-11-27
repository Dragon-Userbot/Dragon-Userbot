from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
import requests
import asyncio


def getpic(query):
    return eval(requests.get(f"https://nekos.life/api/v2/img/{query}").text)["url"]


@Client.on_message(filters.command("neko", prefix) & filters.me)
async def neko(client: Client, message: Message):
    await message.edit("<code>Wait...</code>")
    try:
        query = message.command[1]
        await message.edit(f"{getpic(query)}", disable_web_page_preview=False)
    except:
        await message.edit("<code>Error\nYou entered the wrong type for it</code>")


@Client.on_message(filters.command("neko_types", prefix) & filters.me)
async def neko_types_func(client: Client, message: Message):
    neko_t = """femdom tickle classic ngif erofeet meow erok poke les hololewd lewdk keta feetg nsfw_neko_gif eroyuri kiss 8ball kuni tits pussy_jpg cum_jpg pussy lewdkemo lizard slap lewd cum cuddle spank smallboobs goose Random_hentai_gif avatar fox_girl nsfw_avatar hug gecg boobs pat feet smug kemonomimi solog holo wallpaper bj woof yuri trap anal baka blowjob holoero feed neko gasm hentai futanari ero solo waifu pwankg eron erokemo"""
    neko_types = ""
    for ntype in neko_t.split():
        neko_types += f"<code>{ntype}</code>  "
    await message.edit(neko_types)


@Client.on_message(filters.command("nekospam", prefix) & filters.me)
async def neko_spam(client: Client, message: Message):
    await message.delete()
    query = " ".join(message.command[2:])
    quantity = int(message.command[1])
    for _ in range(quantity):
        await client.send_message(
            message.chat.id, getpic(query), disable_web_page_preview=False
        )
        await asyncio.sleep(0.2)


modules_help.append(
    {
        "neko": [
            {"neko [type]* [amount of spam]": "For get neko media"},
            {"neko_types": "Available neko types"},
        ]
    }
)
