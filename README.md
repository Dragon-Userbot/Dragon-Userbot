
<h1>Userbot</h1>
<p><b>This repository contains the userbot code as well as instructions for self-deploying the bot</b></p><br>
  


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
cd login
python3 login.py
cd ../
python3 main.py
```
<h2>Custom modules</h2>


To add your modules just put a .py file in  <a href='https://github.com/JoHn-111/Userbot/tree/master/modules'>/modules.</a>This file should have the following code:
```python3
from pyrogram import Message, Filters
from utils import app


@app.on_message(Filters.command('example', ['.']) & Filters.me)
def module_name(client, message):
    message.edit('This is an example module')
    
```
<h2>Thanks to</h2>
<nav>
<li><a href='https://github.com/Legenda24'>Legenda24</a> for the module code <a href=https://github.com/JoHn-111/Userbot/blob/master/modules/text_to_img.py>text_to_img.py</a></li>
</nav>
<h4>Written on <a href='https://github.com/pyrogram/pyrogram'>Pyrogram</a></h4>
