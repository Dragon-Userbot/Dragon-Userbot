from pyrogram import Client, filters
from .utils.utils import modules_help
import requests
import time


def getpic(query):
    return eval(requests.get(f"https://nekos.life/api/v2/img/{query}").text)['url']

@Client.on_message(filters.command(['neko', 'n'], ['.']) & filters.me)
def neko(client, message):
    message.delete()
    query = message.command[1]
    client.send_message(message.chat.id, getpic(query), disable_web_page_preview=False)

@Client.on_message(filters.command(['neko_types', 'nt'], ['.']) & filters.me)
def neko_types_func(client, message):
    n_t = '''<code>femdom tickle classic ngif erofeet meow erok poke les hololewd lewdk keta feetg nsfw_neko_gif eroyuri kiss 8ball kuni tits pussy_jpg cum_jpg pussy lewdkemo lizard slap lewd cum cuddle spank smallboobs goose Random_hentai_gif avatar fox_girl nsfw_avatar hug gecg boobs pat feet smug kemonomimi solog holo wallpaper bj woof yuri trap anal baka blowjob holoero feed neko gasm hentai futanari ero solo waifu pwankg eron erokemo</code>'''
    message.edit(n_t)

@Client.on_message(filters.command(['nekospam', 'ns'], ['.']) & filters.me)
def neko_spam(client, message):
    message.delete()
    query = ' '.join(message.command[2:])
    quantity = int(message.command[1])
    for _ in range(quantity):
        client.send_message(message.chat.id, getpic(query), disable_web_page_preview=False)
        time.sleep(0.2)


modules_help.update({'neko': '''<b>Help for |Neko|\nUsage:</b>
<code>.neko [type]</code>
<b>[For get neko media]</b>
<code>.neko_types</code>
<b>[Available neko types]</b>
<code>.nekospam [amount of spam] [type]</code>
<b>[Spam neko]</b>''', 'neko module': '<b>• Neko</b>:<code> neko, neko_types, nekospam</code>\n'})
