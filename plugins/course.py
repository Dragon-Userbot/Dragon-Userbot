from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


@Client.on_message(filters.command('course', prefix) & filters.me)
async def convert(client: Client, message: Message):
    try:
        await message.edit('<code>Data retrieval...</code>')
        name = message.command[1]

        if name == "btc":
            name = "1₿"
            link = f"https://ru.investing.com/crypto/bitcoin"
        else:    
            link = f"https://ru.investing.com/currencies/{name}-rub"

        full_page = requests.get(link, headers=headers, timeout=3)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        rub = soup.find('span', id='last_last')
        await message.edit(f'<b>{name} now is </b><code> {rub} </code><b> rub</b>')
    except:
        await message.edit('<code>ERROR</code>')


modules_help.update(
    {
        'course': '''course [currency] - Transfer from any state currency to the ruble]\n[Dont use more than 10 times per minute''',
        'course module': 'Course: course',
    }
)
