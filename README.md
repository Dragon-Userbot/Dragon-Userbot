<p align="center">
        <img src="https://telegra.ph/file/97ba4adfdf5ac59a213d9.png" width="500" alt="Dragon-Userbot">
    </a>
    <br>
    <b>Dragon-Userbot</b>
    <br>
    <b>Telegram userbot with the easiest installation</b>
    <br>
    <a href='https://github.com/JoHn-111/Dragon-Userbot/tree/master#installation-not-the-final-version'>
        Installation
    </a>
    •
    <a href="https://github.com/JoHn-111/Dragon-Userbot/releases">
        Releases
    </a>
    •
    <a href="https://t.me/Dragon_Userbot_chat">
        Community
    </a>
    •
    <a href='https://github.com/JoHn-111/Dragon-Userbot/tree/master#custom-modules'>
        Custom modules
    </a>
</p>



<h2>Installation (Linux & wsl only)</h2>

<code>  pip3 install wheel</code>

<code>  pkg install libjpeg-turbo</code>

<code> sudo apt update</code>

<code>  sudo apt install ffmpeg</code>

<code>  git clone https://github.com/Dragon-Userbot/Dragon-Userbot.git</code>

<code>  cd Dragon-Userbot/</code>

<code>  pip3 install -r requirements.txt</code>

<code>  python3 main.py</code>

<code>  .help</code> (in telegram chat)

Subsequent launch:

<code>  cd Dragon-Userbot/</code>

<code>  python3 main.py</code>


<h2>Custom modules</h2>



To add your modules just put a .py file in  <a href='https://github.com/JoHn-111/Userbot/tree/master/plugins'>/plugins.</a>This file should have the following code:


```python3
from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help
from .utils.utils import requirements_list

# packages from PyPi
#import example_1
#import example_2


@Client.on_message(filters.command('example_edit', ['.']) & filters.me)
async def example_edit(client: Client, message: Message):
    await message.edit('<code>This is an example module</code>')


@Client.on_message(filters.command('example_send', ['.']) & filters.me)
async def example_send(client: Client, message: Message):
    await client.send_message(message.chat.id, '<b>This is an example module</b>')

# This adds instructions for your module
modules_help.update({'example': '''example_send - example send, example_edit - example edit''',
                     'example module': 'Example send: example_send, example_edit'})

#'module_name': '''comand_1 - description, comand_2 - description''',
#        │          'module_name module': 'Example send: example_send, example_edit'
#        │                 │        │
#        │                 │        │
#     module_name(only snake_case)  └─ module (here the word 'module' is required)
#
#If you need to put a HYPHEN inside the description, then put not a standard sign, but this ->[ – ]
#If you need to put a COMMA inside the description, then put not a standard sign, but this ->[ ，]

# If your custom module requires packages from PyPi, write the names of the packages in these functions
# requirements_list.append('example_1')
# requirements_list.append('example_2')
# etc
```
<h2>Groups and support</h2>
<p>Latest news on the official telegram <a href='https://t.me/Dragon_Userbot'>channel</a></p>

<p>Discussion in the official telegram <a href='https://t.me/Dragon_Userbot_chat'>chat</a></p>

<h2>Credits</h2>
<nav>
<li><a href='https://github.com/Taijefx34'>Taijefx34</a></li>
<li><a href='https://github.com/LaciaMemeFrame'>LaciaMemeFrame</a></li>
</nav>
<h4>❤️Written on <a href='https://github.com/pyrogram/pyrogram'>Pyrogram</a> and <a href='https://github.com/MarshalX/tgcalls/tree/main/pytgcalls'>pytgcalls</a>❤️</h4>
