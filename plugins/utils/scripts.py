from pyrogram import Client, filters


date_dict = {}

@Client.on_message(filters.chat("@creationdatebot"), group=-1)
def get_date(client, message):
    client.read_history("@creationdatebot")
    date_dict.update({"date": message.text})