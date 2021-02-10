from pyrogram import Client, filters
from .utils.utils import modules_help
import requests
from bs4 import BeautifulSoup 


DOLLAR = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
EUR = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B5&aqs=chrome.1.69i57j0i433l5j0i395i433l2j0i131i395i433.3879j1j7&sourceid=chrome&ie=UTF-8'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


@Client.on_message(filters.command('usd', ['.']) & filters.me)
async def usd(client, message):
	try:
		await message.edit('<code>Data retrieval...</code>')
		full_page = requests.get(DOLLAR, headers=headers, timeout=0.5)
		soup = BeautifulSoup(full_page.content, 'html.parser')
		rub = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		await message.edit(f'<b>One dollar now is </b><code>{rub}</code><b> rub</b>')
	except:
		await message.edit('<code>Too many requests please try again later</code>')

@Client.on_message(filters.command('eur', ['.']) & filters.me)
async def eur(client, message):
	try:
		await message.edit('<code>Data retrieval...</code>')
		full_page = requests.get(EUR, headers=headers, timeout=0.5)
		soup = BeautifulSoup(full_page.content, 'html.parser')
		rub = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		await message.edit(f'<b>One euro now is </b><code>{rub}</code><b> rub</b>')
	except:
		await message.edit('<code>Too many requests please try again later</code>')


modules_help.update({'course': '''<b>Help for |course|\nUsage:</b>
<code>.usd<code>
<b>[For get course usd to rub]</b>
<code>.eur</code>
<b>[For get course eur to rub]</b>
<b>[Dont use more than 10 times per minute]</b>''', 'course module': '<b>• Course</b>:<code> usd, eur</code>\n'})
