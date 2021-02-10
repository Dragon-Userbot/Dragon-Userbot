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
#requirements_list.append('example_1')
#requirements_list.append('example_2')
#etc
