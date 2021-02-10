import wikipedia
from pyrogram import Client, filters
from .utils.utils import modules_help
from .utils.utils import requirements_list


@Client.on_message(filters.command('wiki', ['.']) & filters.me)
async def wiki(client, message):
	lang = message.command[1]
	user_request = ' '.join(message.command[2:])
	if user_request == '':
		wikipedia.set_lang("ru")
		user_request = ' '.join(message.command[1:])
	try:
		if lang == 'en':
			wikipedia.set_lang("en")

		result = wikipedia.summary(user_request)
		await message.edit(f'''<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{result}</code>''')

	except:
		await message.edit(f'''<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{exc}</code>''')


modules_help.update({'wikipedia': '''<b>Help for |Wikipedia|\nUsage:</b>
<code>.wiki [request]</code>
<b>[Search on the English Wikipedia]</b>
<code>.wiki ru [request]</code>
<b>[Search in Russian Wikipedia]</b>''', 'wikipedia module': '<b>• Wikipedia</b>:<code> wiki</code>\n'})

requirements_list.append('wikipedia')
