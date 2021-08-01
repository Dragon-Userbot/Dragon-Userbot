from pyrogram import Client, idle
import configparser
import datetime
import os
import sys


if len(sys.argv) == 2:
    arg = sys.argv[1]
    config_path = os.path.join(sys.path[0], 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)

    config.set('pyrogram', 'db_url', arg)
    with open(config_path, "w") as config_file:
        config.write(config_file)

    app = Client("my_account")
    app.start()
    app.send_message('me', f'<b>[{datetime.datetime.now()}] Dragon-Userbot launched!\nFor restart, enter:</b>\n <code>cd Dragon-Userbot/ && python main.py</code>')

    app.stop()

    print('Account is successfully linked, for run use: python main.py')
