from pyrogram import Client, filters
from .utils.utils import modules_help
import subprocess
from threading import Thread
import time


def restart(client, message):
    client.restart()
    message.edit('<code>Restart was successful!</code>')
    
    
def update_restart(client, message):
    client.restart()
    message.edit('<code>Restart was successful!</code>')
    time.sleep(3)
    message.edit('<code>Update process completed!</code>')
    
    
@Client.on_message(filters.command('restart', ['.']) & filters.me)
def restart_comand(client, message):
    message.edit('<code>Restarting...</code>')
    Thread(target=restart, args=(client, message)).start()
    
    
@Client.on_message(filters.command('update', ["."]) & filters.me)
def update(client, message):
    message.edit('<code>Updating...</code>')
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    for lib in range(len(requirements_list)):
        process = subprocess.Popen(["pip", "install", f"{requirements_list[lib]}"], stdout=subprocess.PIPE)
        output = process.communicate()[0]
    message.edit('<code>Restarting...</code>')
    Thread(target=update_restart, args=(client, message)).start()
    
    
modules_help.update({'updater': '''<b>Help for |Updater|\nUsage:</b>
<code>.update</code>
<b>[Updating the userbot. If new modules are available, they will be installed]</b>
<code>.restart</code>
<b>[Restart userbot]</b>''', 'updater module': '<b>• Updater</b>:<code> update, restart</code>\n'})
