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
    <br>
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge" alt="Code style">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Dragon-Userbot/Dragon-Userbot?style=for-the-badge">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Dragon-Userbot/Dragon-Userbot?style=for-the-badge">
</p>




<h1>About</h1>
<p>Dragon-Userbot is a Telegram userbot (in case you didn't know, selfbot/userbot are used to automate user accounts).
So how does it work? It works in a very simple way, using the pyrogram library, a python script connects to your account (creating a new session) and catches your commands.

Using selfbot/userbot is against Telegram's Terms of Service, and you may get banned for using it if you're not careful.

The developers are not responsible for any consequences you may encounter when using Dragon-Userbot. We are also not
responsible for any damage to chat rooms caused by using this userbot.</p>



<h1>Installation</h1>
<h2>lavHost</h2>

<a href="https://t.me/lavhostbot?start=RHJhZ29u"><img src="https://f.lavhost.ml/images/install_to_lavhost.png"></a>


<h2>Linux, Termux (use <a href='https://f-droid.org/en/packages/com.termux/'>f-droid</a> version) and Windows [only wsl]</h2>

<pre><code>apt-get upgrade -y && apt-get update && apt install git && git clone https://github.com/Dragon-Userbot/Dragon-Userbot.git && cd Dragon-Userbot/ && bash install.sh
</code></pre>

<h2>macOS [<a href='https://brew.sh'>brew</a>]</h2>
<pre><code>brew install git && git clone https://github.com/Dragon-Userbot/Dragon-Userbot.git && cd Dragon-Userbot && brew install python@3.8 && pip3 install --upgrade pip && pip3 install wheel && brew install ffmpeg && pip3 install -r requirements.txt && pip3 install -U 'pytgcalls[pyrogram]' && echo Enter your db_url: && read uservar && python3 install.py $uservar
</code></pre>

<p>Next enter mongo_db_url (<a href='https://telegra.ph/How-to-get-Mongodb-URL-and-login-in-telegram-08-01'>How to get Mongodb_URL and login in telegram</a>)</p>

<pre><code>.help</code> (in telegram chat)</pre>

Subsequent launch:

<pre><code>cd Dragon-Userbot/</code></pre>

<pre><code>python3 main.py</code></pre>


<h1>Custom modules</h1>


<p>To add your module to the bot, create a pull request in the <a href='https://github.com/Dragon-Userbot/custom_modules/'>custom_modules</a> repository</p>

```python3
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


# if your module has packages from PyPi

# from utils.scripts import import_library
# example_1 = import_library("example_1")
# example_2 = import_library("example_2")

# import_library() will automatically install required library
# if it isn't installed


@Client.on_message(filters.command("example_edit", prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    await message.edit("<code>This is an example module</code>")


@Client.on_message(filters.command("example_send", prefix) & filters.me)
async def example_send(client: Client, message: Message):
    await client.send_message(message.chat.id, "<b>This is an example module</b>")


# This adds instructions for your module
modules_help["example"] = {
    "example_send": "example send",
    "example_edit": "example edit",
}

# modules_help["example"] = { "example_send [text]": "example send" }
#                  |            |              |        |
#                  |            |              |        └─ command description
#           module_name         command_name   └─ optional command arguments
#        (only snake_case)   (only snake_case too)
```

<h2>Groups and support</h2>
<p><a href='https://t.me/Dragon_Userb0t'>Channel</a> with latest news on the official telegram [ru/en]</p>

<p><a href='https://t.me/Dragon_Userb0t_modules'>Channel</a> with custom modules [ru/en] </p>

<p><a href='https://t.me/Dragon_Userb0t_chat'>Discussion</a> in the official telegram chat [ru]</p>

<p><a href='https://t.me/Dragon_Userbot_ch0t_en'>Discussion</a> in the official telegram chat [en]</p>

<h2>Credits</h2>
<nav>
<li><a href='https://github.com/Taijefx34'>Taijefx34</a></li>
<li><a href='https://github.com/LaciaMemeFrame'>LaciaMemeFrame</a></li>
<li><a href="https://github.com/KurimuzonAkuma">KurimuzonAkuma</a></li>
<li>asphy <a href='https://t.me/LKRinternationalrunetcomphinc'>tg</a> and <a href='https://ru.namemc.com/profile/asphyxiamywife.1'>namemc</a></li>
<li><a href='http://t.me/fuccsoc2'>fuccsoc</a></li>
</nav>
<h4>Written on <a href='https://github.com/pyrogram/pyrogram'>Pyrogram❤️</a> and <a href='https://github.com/MarshalX/tgcalls/tree/main/pytgcalls'>pytgcalls❤️</a></h4>
