from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from .utils.help_formatting import help_formatting


@Client.on_message(filters.command(["help", "h"], prefix) & filters.me)
async def help(client, message: Message):
    module_name = " ".join(message.command[1:])
    if module_name == "":
        messages = [
            f"""<b>Help for <a href="https://t.me/Dragon_Userbot_chat">Dragon-Userbot</a></b>\n<b>For more help on how to use a command, type </b> <code>{prefix}help [module]</code>\n\n<b>Available Modules:</b>\n"""
        ]
        msg_cnt = 0
        for mod in modules_help:
            help_message = (
                "<b>• "
                + list(mod.keys())[0].title()
                + ": </b>"
                + " ".join(
                    [
                        "<code>" + prefix + str(cmd.split()[0]) + "</code>"
                        for cmd in [
                            list(rc.keys())[0] for rc in list(mod.values()).pop(0)
                        ]
                    ]
                )
                + "\n"
            )
            if len(messages[msg_cnt] + help_message) < 2048:
                messages[msg_cnt] = messages[msg_cnt] + help_message
            else:
                msg_cnt += 1
                messages.append(help_message)
        tc = """\nThe number of modules in the userbot: """ + str(
            float(len(modules_help))
        )
        if len(messages[msg_cnt] + tc) < 2048:
            messages[msg_cnt] += tc
        else:
            messages.append(tc)
        await message.edit(
            messages[0], parse_mode="HTML", disable_web_page_preview=True
        )
        messages.pop(0)
        for msg in messages:
            await message.reply(msg, parse_mode="HTML", disable_web_page_preview=True)
    else:
        text = f"<b>Help for <i>{module_name}</i>\n\nUsage:</b>\n"
        found = False
        for mh in modules_help:
            if list(mh.keys())[0].lower() == module_name.lower():
                found = True
                cmds = list(mh.values()).pop(0)
                for u_cmd in cmds:
                    cmd = list(u_cmd.items())[0]
                    text += f"""<code>{prefix + cmd[0]}</code> - <i>{cmd[1]}</i>\n"""
        if found:
            await message.edit(text, parse_mode="HTML")
        else:
            await message.edit(f"<b>Module <i>{module_name}</i> not found!</b>")


modules_help.append(
    {"help": [{"help [module name]": "To get help. Module name isn't required."}]}
)
