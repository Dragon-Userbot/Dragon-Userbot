from pyrogram import Client, filters


date_dict = {}

@Client.on_message(filters.chat("@creationdatebot"), group=-1)
async def get_date(client, message):
    await client.read_history("@creationdatebot")
    date_dict.update({"date": message.text})
