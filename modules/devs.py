#  Dragon-Userbot - telegram userbot
#  Copyright (C) 2020-present Dragon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import re
import subprocess
import sys
import traceback
from subprocess import Popen, PIPE, TimeoutExpired
from time import perf_counter
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from io import StringIO
from inspect import getfullargspec
from pyrogram import filters
from time import time



async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Client.on_message(filters.command("eval", prefix) & filters.me)
async def evaluate(client, message):
    status_message = await message.edit("`Running ...`")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>Command:</b>\n<code>{cmd}</code>\n\n<b>OUTPUT</b>:\n<code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await status_message.delete()
    else:
        await status_message.edit(final_output)


@Client.on_message(filters.command("sh", prefix) & filters.me)
async def terminal(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `.sh echo owo`")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""",
x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await message.edit(
                    """
**Error:**
```{}```
""".format(err)
                )
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await message.edit("""**Error:**\n```{}```""".format("".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="`Output file`",
            )
            os.remove("output.txt")
            return
        await message.edit(f"**Output:**\n```{output}```")
    else:
        await message.edit("**Output:**\n`No Output`")


modules_help["devs"] = {
        "sh [command]": "Execute command in shell",
        "eval [command]": "Execute python commands",
}
