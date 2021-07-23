from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from .utils.utils import requirements_list

# packages from PyPi
#import example_1
#import example_2



@Client.on_message(filters.command('example_edit', prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    await message.edit('<code>This is an example module</code>')


@Client.on_message(filters.command('example_send', prefix) & filters.me)
async def example_send(client: Client, message: Message):
    await client.send_message(message.chat.id, '<b>This is an example module</b>')

# This adds instructions for your module
modules_help.update({'example': '''example_send - example send, example_edit - example edit''',
                     'example module': 'Example: example_send, example_edit'})

#'module_name': '''comand_1 - description, comand_2 - description''',
#        │          'module_name module': 'Example send: example_send, example_edit\n\n'
#        │                 │        │
#        │                 │        │
#     module_name(only snake_case)  └─ module (here the word 'module' is required)


# If your custom module requires packages from PyPi, write the names of the packages in these functions
# requirements_list.append('example_1')
# requirements_list.append('example_2')
# etc
