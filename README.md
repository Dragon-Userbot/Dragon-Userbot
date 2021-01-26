
<h1>Userbot</h1>

<h3>This repository contains the custom bot code, instructions on how to deploy the bot yourself, and an example of required code in custom modules</h3><br>
  

<nav>
<li><a href='https://github.com/JoHn-111/Userbot/tree/master#installation'>Installation</a></li>
<li><a href='https://github.com/JoHn-111/Userbot/tree/master#custom-modules'>Custom modules</a></li>
<li><a href='https://github.com/JoHn-111/Userbot#credits'>Credits</a></li>
  
</nav>


<h2>Installation (not the final version)</h2>
<code>  git clone https://github.com/JoHn-111/Userbot.git</code>

<code>  cd Userbot /</code>

<code>  pip3 install -r requirements.txt</code>

<code>  vim config.ini</code> (or other editor)

<p>Insert api_id and api_hash (my.telegram.org)</p>

<code>  python3 main.py</code>

Subsequent launch:

<code>  cd Userbot /</code>

<code>  python3 main.py</code>


<h2>Custom modules</h2>



To add your modules just put a .py file in  <a href='https://github.com/JoHn-111/Userbot/tree/master/plugins'>/plugins.</a>This file should have the following code:


```python3
from pyrogram import Client, filters
from .utils.utils import modules_help
from .utils.utils import requirements_list

#packages from PyPi
import example_1
import example_2


@Client.on_message(filters.command('example', ['.']) & filters.me)
def module_name(client, message):
    message.edit('This is an example module')


#This adds instructions for your module
modules_help.update({'example': '''<b>Help for |example|\nUsage:</b>
<code>.example</code>
<b>[To get example]</b>''', 'example module': '<b>• Example</b>:<code> example</code>\n'})

#If your custom module requires packages from PyPi, write the names of the packages in these functions
requirements_list.append('example_1')
requirements_list.append('example_2')
#etc
```
<h2>Credits</h2>
<nav>
<li><a href='https://github.com/Legenda24'>Legenda×24</a></li>
<li><a href='https://github.com/LaciaMemeFrame'>LaciaMemeFrame</a></li>
</nav>
<h4>Written on <a href='https://github.com/pyrogram/pyrogram'>Pyrogram</a></h4>
