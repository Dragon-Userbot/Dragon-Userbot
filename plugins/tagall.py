from pyrogram import Client, filters
from .utils.utils import modules_help
import asyncio


@Client.on_message(filters.command('tagall', ['.']) & filters.me)
async def tagall(client, message):
	await message.delete()
	chat_id = message.chat.id
	string = ""
	limit = 1
	icm = client.iter_chat_members(chat_id)
	async for member in icm:
		tag = member.user.username
		if limit <= 5:
			if tag != None:
				string += f"@{tag}\n"
			else:
				string += f"{member.user.mention}\n"
			limit += 1
		else:
			await client.send_message(chat_id, text=string)
			limit = 1
			string = ""
			await asyncio.sleep(2)


modules_help.update({'tagall': '''<b>Help for |tagall|\nUsage:</b>
<code>.tagall</code>
<b>[Tag all members]</b>''', 'tagall module': '<b>• Tagall</b>:<code> tagall</code>\n'})
