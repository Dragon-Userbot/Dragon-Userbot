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

import hashlib
import os

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.scripts import restart
from utils.misc import modules_help, prefix


BASE_PATH = os.path.abspath(os.getcwd())


@Client.on_message(filters.command(["modhash", "mh"], prefix) & filters.me)
async def get_mod_hash(_, message: Message):
    if len(message.command) == 1:
        return
    url = message.command[1].lower()
    resp = requests.get(url)
    if not resp.ok:
        await message.edit(
            f"<b>Troubleshooting with downloading module <code>{url}</code></b>"
        )
        return

    await message.edit(
        f"<b>Module hash: <code>{hashlib.sha256(resp.content).hexdigest()}</code>\n"
        f"Link: <code>{url}</code>\nFile: <code>{url.split('/')[-1]}</code></b>"
    )


@Client.on_message(filters.command(["loadmod", "lm"], prefix) & filters.me)
async def loadmod(_, message: Message):
    if (
        not (
            message.reply_to_message
            and message.reply_to_message.document
            and message.reply_to_message.document.file_name.endswith(".py")
        )
        and len(message.command) == 1
    ):
        await message.edit("<b>Specify module to download</b>")
        return

    if len(message.command) > 1:
        url = message.command[1].lower()

        if url.startswith(
            "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/"
        ):
            module_name = url.split("/")[-1].split(".")[0]
        elif "/" not in url and "." not in url:
            module_name = url.lower()
            url = f"https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/{module_name}.py"
        else:
            modules_hashes = requests.get(
                "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/modules_hashes.txt"
            ).text
            resp = requests.get(url)

            if not resp.ok:
                await message.edit(
                    f"<b>Troubleshooting with downloading module <code>{url}</code></b>"
                )
                return

            if hashlib.sha256(resp.content).hexdigest() not in modules_hashes:
                return await message.edit(
                    "<b>Only <a href=https://github.com/Dragon-Userbot/custom_modules/tree/main/modules_hashes.txt>"
                    "verified</a> modules or from the official "
                    "<a href=https://github.com/Dragon-Userbot/custom_modules>"
                    "custom_modules</a> repository are supported!</b>",
                    disable_web_page_preview=True,
                )

            module_name = url.split("/")[-1].split(".")[0]

        resp = requests.get(url)
        if not resp.ok:
            await message.edit(f"<b>Module <code>{module_name}</code> is not found</b>")
            return

        if not os.path.exists(f"{BASE_PATH}/modules/custom_modules"):
            os.mkdir(f"{BASE_PATH}/modules/custom_modules")

        with open(f"./modules/custom_modules/{module_name}.py", "wb") as f:
            f.write(resp.content)
    else:
        file_name = await message.reply_to_message.download()
        module_name = message.reply_to_message.document.file_name[:-3]

        with open(file_name, "rb") as f:
            content = f.read()

        modules_hashes = requests.get(
            "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/modules_hashes.txt"
        ).text

        if hashlib.sha256(content).hexdigest() not in modules_hashes:
            os.remove(file_name)
            return await message.edit(
                "<b>Only <a href=https://github.com/Dragon-Userbot/custom_modules/tree/main/modules_hashes.txt>"
                "verified</a> modules or from the official "
                "<a href=https://github.com/Dragon-Userbot/custom_modules>"
                "custom_modules</a> repository are supported!</b>",
                disable_web_page_preview=True,
            )
        else:
            os.rename(file_name, f"./modules/custom_modules/{module_name}.py")

    await message.edit(f"<b>The module <code>{module_name}</code> is loaded!</b>")
    restart()


@Client.on_message(filters.command(["unloadmod", "ulm"], prefix) & filters.me)
async def unload_mods(_, message: Message):
    if len(message.command) <= 1:
        return

    module_name = message.command[1].lower()

    if module_name.startswith(
        "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/"
    ):
        module_name = module_name.split("/")[-1].split(".")[0]

    if os.path.exists(f"{BASE_PATH}/modules/custom_modules/{module_name}.py"):
        os.remove(f"{BASE_PATH}/modules/custom_modules/{module_name}.py")
        await message.edit(f"<b>The module <code>{module_name}</code> removed!</b>")
        restart()
    elif os.path.exists(f"{BASE_PATH}/modules/{module_name}.py"):
        await message.edit(
            "<b>It is forbidden to remove built-in modules, it will disrupt the updater</b>"
        )
    else:
        await message.edit(f"<b>Module <code>{module_name}</code> is not found</b>")


@Client.on_message(filters.command(["loadallmods"], prefix) & filters.me)
async def load_all_mods(_, message: Message):
    await message.edit("<b>Fetching info...</b>")

    if not os.path.exists(f"{BASE_PATH}/modules/custom_modules"):
        os.mkdir(f"{BASE_PATH}/modules/custom_modules")

    modules_list = requests.get(
        "https://api.github.com/repos/Dragon-Userbot/custom_modules/contents/"
    ).json()

    new_modules = {}
    for module_info in modules_list:
        if not module_info["name"].endswith(".py"):
            continue
        if os.path.exists(f'{BASE_PATH}/modules/custom_modules/{module_info["name"]}'):
            continue
        new_modules[module_info["name"][:-3]] = module_info["download_url"]
    if not new_modules:
        return await message.edit("<b>All modules already loaded</b>")

    await message.edit(f'<b>Loading new modules: {" ".join(new_modules.keys())}</b>')
    for name, url in new_modules.items():
        with open(f"./modules/custom_modules/{name}.py", "wb") as f:
            f.write(requests.get(url).content)

    await message.edit(
        f'<b>Successfully loaded new modules: {" ".join(new_modules.keys())}</b>'
    )
    restart()


@Client.on_message(filters.command(["updateallmods"], prefix) & filters.me)
async def updateallmods(_, message: Message):
    await message.edit("<b>Updating modules...</b>")

    if not os.path.exists(f"{BASE_PATH}/modules/custom_modules"):
        os.mkdir(f"{BASE_PATH}/modules/custom_modules")

    modules_installed = list(os.walk("modules/custom_modules"))[0][2]

    if not modules_installed:
        return await message.edit("<b>You don't have any modules installed</b>")

    for module_name in modules_installed:
        if not module_name.endswith(".py"):
            continue

        resp = requests.get(
            f"https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/{module_name}"
        )
        if not resp.ok:
            modules_installed.remove(module_name)
            continue

        with open(f"./modules/custom_modules/{module_name}", "wb") as f:
            f.write(resp.content)

    await message.edit(f"<b>Successfully updated {len(modules_installed)} modules</b>")


modules_help["loader"] = {
    "loadmod [module_name]*": "Download module.\n"
    "Only modules from the official custom_modules repository and proven "
    "modules whose hashes are in modules_hashes.txt are supported",
    "unloadmod [module_name]*": "Delete module",
    "modhash [link]*": "Get module hash by link",
    "loadallmods": "Load all custom modules (use it at your own risk)",
    "updateallmods": "Update all custom modules",
}
