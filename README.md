<p align="center">
        <img src="https://telegra.ph/file/97ba4adfdf5ac59a213d9.png" width="500" alt="Dragon-Userbot">
    </a>
    <br>
    <b>Dragon-Userbot</b>
    <br>
    <b>Telegram userbot with the easiest installation</b>
    <br>
    <a href='https://github.com/Dragon-Userbot/Dragon-Userbot#installation'>
        Installation
    </a>
    •
    <a href="https://github.com/Dragon-Userbot/Dragon-Userbot/releases">
        Releases
    </a>
    •
    <a href="https://github.com/Dragon-Userbot/Dragon-Userbot#groups-and-support">
        Community
    </a>
    •
    <a href='https://github.com/Dragon-Userbot/Dragon-Userbot#custom-modules'>
        Custom modules
    </a>
</p>


<h1>Installation</h1>
<h2>Linux, Termux and Windows [only wsl]</h2>

<pre><code>apt-get upgrade -y && apt-get update && apt install git && git clone https://github.com/john-phonk/Dragon-Userbot && cd Dragon-Userbot/ && sh install.sh
</code></pre>

<h2>macOS [<a href='https://brew.sh'>brew</a>]</h2>
<pre><code>brew install git && git clone https://github.com/Dragon-Userbot/Dragon-Userbot.git && cd Dragon-Userbot && brew install python@3.8 && pip3 install --upgrade pip && pip3 install wheel && brew install ffmpeg && pip3 install -r requirements.txt && pip3 install -U 'pytgcalls[pyrogram]' && echo Enter your db_url: && read uservar && python3 install.py $uservar
</code></pre>

<p>Next enter mongo_db_url (<a href='https://telegra.ph/How-to-get-Mongodb-URL-and-login-in-telegram-08-01'>How to get Mongodb_URL and login in telegram</a>)</p>

<pre><code>.help</code> (in telegram chat)</pre>

Subsequent launch:

<pre><code>cd Dragon-Userbot/</code></pre>

<pre><code>python3 main.py</code></pre>


<h2>Custom modules</h2>


<p>To add your module to the bot, create a pull request in the <a href='https://github.com/Dragon-Userbot/custom_modules/'>custom_modules</a> repository</p>
<p>Either send the module and its hash to me (<a href='https://t.me/john_phonk'>@john_phonk</a>) details in this <a href='https://t.me/Dragon_Userbot/65'>post</a></p>

```python3
from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help
from ..utils.utils import requirements_list

# packages from PyPI
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
                     'example module': 'Example_send: example_send, example_edit'})

#'module_name': '''comand_1 - description, comand_2 - description''',
#        │          'module_name module': 'Example_send: example_send, example_edit'
#        │                 │        │
#        │                 │        │
#     module_name(only snake_case)  └─ module (here the word 'module' is required)
#
#If you need to put a HYPHEN inside the description, then put not a standard sign, but this ->[ – ]
#If you need to put a COMMA inside the description, then put not a standard sign, but this ->[ ，]

# If your custom module requires packages from PyPI, write the names of the packages in these functions
# requirements_list.append('example_1')
# requirements_list.append('example_2')
# etc
```
<h2>Groups and support</h2>
<p><a href='https://t.me/Dragon_Userbot'>Channel</a> with latest news on the official telegram [ru/en]</p>

<p><a href='https://t.me/Dragon_Userbot_modules'>Channel</a> with custom modules [ru/en] </p>

<p><a href='https://t.me/dRaGoN_uB_cHaNgElOg'>Channel</a> with ChAnGeLoGs!) [♿AsPhY♿] </p>

<p><a href='https://t.me/Dragon_Userbot_chat'>Discussion</a> in the official telegram chat [ru]</p>

<p><a href='https://t.me/Dragon_Userbot_chat_en'>Discussion</a> in the official telegram chat [en]</p>

<h2>Credits</h2>
<nav>
<li><a href='https://github.com/Taijefx34'>Taijefx34</a></li>
<li><a href='https://github.com/LaciaMemeFrame'>LaciaMemeFrame</a></li>
<li><a href='https://t.me/nalinor'>nalinor</a></li>
<li>asphy <a href='https://t.me/LKRinternationalrunetcomphinc'>tg</a> and <a href='https://ru.namemc.com/profile/asphyxiamywife.1'>namemc</a></li>
</nav>
<h4>Written on <a href='https://github.com/pyrogram/pyrogram'>Pyrogram❤️</a> and <a href='https://github.com/MarshalX/tgcalls/tree/main/pytgcalls'>pytgcalls❤️</a></h4>
