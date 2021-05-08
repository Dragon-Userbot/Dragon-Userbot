<p align="center">
    <a href="https://github.com/pyrogram/pyrogram">
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



<h2>Installation (not the final version)</h2>

<code>  pip install wheel</code>

<code>  pkg install libjpeg-turbo</code>


<code>  git clone https://github.com/JoHn-111/Dragon-Userbot.git</code>

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
from .utils.utils import modules_help
from .utils.utils import requirements_list

#packages from PyPi
#import example_1
#import example_2


@Client.on_message(filters.command('example', ['.']) & filters.me)
async def module_name(client, message):
    await message.edit('This is an example module')


#This adds instructions for your module
modules_help.update({'example': '''<b>Help for |example|\nUsage:</b>
<code>.example</code>
<b>[Example module help]</b>''', 'example module': '<b>• Example</b>:<code> example</code>\n'})

#If your custom module requires packages from PyPi, write the names of the packages in these functions
requirements_list.append('example_1')
requirements_list.append('example_2')
#etc
```
<h2>Groups and support</h2>
<p>Latest news on the official telegram <a href='https://t.me/Dragon_Userbot'>channel</a></p>

<p>Discussion in the official telegram <a href='https://t.me/Dragon_Userbot_chat'>chat</a></p>

<h2>Credits</h2>
<nav>
<li><a href='https://github.com/Legenda24'>Legenda×24</a></li>
<li><a href='https://github.com/LaciaMemeFrame'>LaciaMemeFrame</a></li>
</nav>
<h4>Written on <a href='https://github.com/pyrogram/pyrogram'>Pyrogram</a></h4>
