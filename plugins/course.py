from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
import requests
from bs4 import BeautifulSoup


usd = 'https://ru.investing.com/currencies/usd-rub'
eur = 'https://ru.investing.com/currencies/eur-rub'
btc = 'https://ru.investing.com/crypto/bitcoin/btc-rub'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


@Client.on_message(filters.command('course', prefix) & filters.me)
async def convert(client: Client, message: Message):
    try:
        await message.edit('<code>Подождите...</code>')
        if message.command[1] == 'usd':
            name = '1$'
            link = usd
        elif message.command[1] == 'eur':
            name = '1€'
            link = eur
        elif message.command[1] == 'btc':
            name = '1₿'
            link = btc
        full_page = requests.get(link, headers=headers, timeout=1)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        rub = soup.find('span', id='last_last')
        await message.edit(f'<b>{name} стоит </b><code> {rub} </code><b> рублей</b>')
    except:
        await message.edit('<code>ERROR ЖОПЫ</code>')


modules_help.update({'course': '''usd - Для перевода из доллара в рубль, 
    eur - Для перевода из евро в рубль,
    btc - Для перевода из биткойна в рубль]\n[Не используйте чаще, чем 10 раз в минуту!''',
    'course module': 'Course: usd, eur, btc'})
