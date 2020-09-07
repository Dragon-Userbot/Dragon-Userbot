
<h1>Userbot</h1>
<h2>This is not the final version!</h2>
<h3>This repository contains the custom bot code, instructions on how to deploy the bot yourself, and an example of required code in custom modules</h3><br>
  


<nav>
<li><a href='https://github.com/JoHn-111/Userbot/tree/master#installation'>Installation</a></li>
<li><a href='https://github.com/JoHn-111/Userbot/tree/master#custom-modules'>Custom modules</a></li>
<li><a href='https://github.com/JoHn-111/Userbot/tree/master#thanks-to'>Thanks</a></li>
  
</nav>


<h2>Installation</h2>


```bash
git clone https://github.com/JoHn-111/Userbot.git
cd Userbot
pip3 install -r requirements.txt
python3 main.py
```
<h2>Custom modules</h2>


To add your modules just put a .py file in  <a href='https://github.com/JoHn-111/Userbot/tree/master/plugins'>/plugins.</a>This file should have the following code:
```python3
from pyrogram.types import Message
from pyrogram import Client, filters


@Client.on_message(filters.command('example', ['.']) & filters.me)
def module_name(client, message):
    message.edit('This is an example module')
    
```
<h2>Thanks to</h2>
<nav>
<li><a href='https://github.com/Legenda24'>Legenda24</a> for the module code <a href='https://github.com/JoHn-111/Userbot/blob/master/plugins/text_to_img.py'>text_to_img.py</a></li>
</nav>
<h4>Written on <a href='https://github.com/pyrogram/pyrogram'>Pyrogram</a></h4>
