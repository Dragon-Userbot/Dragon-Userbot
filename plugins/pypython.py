from pyrogram.types import Message
from pyrogram import Client, filters
import time

from io import StringIO
import sys


@Client.on_message(filters.command('ex', ['.']) & filters.me)
def user_exec(client, message):
    code = ''
    try:
        code = message.text.split(".ex\n")[1]
    except IndexError:
        try:
            code = message.text.split(".ex ")[1]
        except IndexError:
            pass

    if message.reply_to_message:
        code = message.reply_to_message.text
        result = sys.stdout = StringIO()
        try:
            exec(code)
            message.edit(f'''<b>Code:</b>
<code>{code}</code>
<b>Result</b>:
<code>{result.getvalue()}</code>
''')
        except:
            message.edit(f'''<b>Code:</b>
<code>{code}</code>
<b>Result</b>:
<code>{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}</code>
''')

    else:
        result = sys.stdout = StringIO()
        try:
            exec(code)
            message.edit(f'''<b>Code:</b>
<code>{code}</code>
<b>Result</b>:
<code>{result.getvalue()}</code>
''')
        except:
            message.edit(f'''<b>Code:</b>
<code>{code}</code>
<b>Result</b>:
<code>{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}</code>
''')
