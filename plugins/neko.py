from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help
import requests
import asyncio


def getpic(query):
    return eval(requests.get(f"https://nekos.life/api/v2/img/{query}").text)['url']


@Client.on_message(filters.command('neko', ['.']) & filters.me)
async def neko(client: Client, message: Message):
    await message.delete()
    query = message.command[1]
    await client.send_message(message.chat.id, getpic(query), disable_web_page_preview=False)


@Client.on_message(filters.command('neko_types', ['.']) & filters.me)
async def neko_types_func(client: Client, message: Message):
    n_t = '''<code>femdom tickle classic ngif erofeet meow erok poke les hololewd lewdk keta feetg nsfw_neko_gif eroyuri kiss 8ball kuni tits pussy_jpg cum_jpg pussy lewdkemo lizard slap lewd cum cuddle spank smallboobs goose Random_hentai_gif avatar fox_girl nsfw_avatar hug gecg boobs pat feet smug kemonomimi solog holo wallpaper bj woof yuri trap anal baka blowjob holoero feed neko gasm hentai futanari ero solo waifu pwankg eron erokemo</code>'''
    await message.edit(n_t)


@Client.on_message(filters.command('nekospam', ['.']) & filters.me)
async def neko_spam(client: Client, message: Message):
    await message.delete()
    query = ' '.join(message.command[2:])
    quantity = int(message.command[1])
    for _ in range(quantity):
        await client.send_message(message.chat.id, getpic(query), disable_web_page_preview=False)
        await asyncio.sleep(0.2)


modules_help.update({'neko': '''neko [type] - For get neko media, neko_types - Available neko types, nekospam [amount of spam] [type] - Spam''',
                     'neko module': 'Neko: neko, neko_types, nekospam'})
