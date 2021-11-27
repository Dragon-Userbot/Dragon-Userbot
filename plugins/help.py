from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from .utils.help_formatting import help_formatting


@Client.on_message(filters.command(["help", "h"], prefix) & filters.me)
async def help(client, message: Message):
    module_name = " ".join(message.command[1:])
    help_message = f"""<b>Help for <a href="https://t.me/Dragon_Userbot_chat">Dragon-Userbot</a></b>\n"""
    help_message += f"""<b>For more help on how to use a command, type </b> <code>{prefix}help [module]</code>\n\n"""
    help_message += "<b>Available Modules:</b>\n"
    if module_name == "":
        for mod in modules_help:
            help_message += (
                "<b>"
                + list(mod.keys())[0]
                + ": </b>"
                + ", ".join(
                    [
                        "<code>" + prefix + str(cmd.split()[0]) + "</code>"
                        for cmd in [
                            list(rc.keys())[0] for rc in list(mod.values()).pop(0)
                        ]
                    ]
                )
                + "\n"
            )
        help_message += """\n\nThe number of modules in the userbot: """ + str(
            len(modules_help)
        )
        await message.edit(
            help_message, parse_mode="HTML", disable_web_page_preview=True
        )
    else:
        text = f"<b>Help for <i>{module_name}</i>\n\nUsage:</b>\n"
        found = False
        for mh in modules_help:
            if list(mh.keys())[0].lower() == module_name:
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
