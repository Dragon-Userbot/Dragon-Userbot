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

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.scripts import (
    restart,
    format_exc,
    format_module_help,
    load_module,
    unload_module,
)
from utils.misc import modules_help, prefix
from utils.config import modules_repo_branch

BASE_PATH = os.path.abspath(os.getcwd())


@Client.on_message(filters.command(["loadmod", "lm"], prefix) & filters.me)
async def loadmod(client: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("<b>Specify module to download</b>")
        return

    module_name = message.command[1].lower()
    resp = requests.get(
        "https://raw.githubusercontent.com/Dragon-Userbot"
        f"/custom_modules/{modules_repo_branch}/{module_name}.py"
    )
    if not resp.ok:
        await message.edit(
            f"<b>Module <code>{module_name}</code> is not found</b>"
        )
        return

    if not os.path.exists(f"{BASE_PATH}/modules/custom_modules"):
        os.mkdir(f"{BASE_PATH}/modules/custom_modules")

    with open(f"./modules/custom_modules/{module_name}.py", "wb") as f:
        f.write(resp.content)

    try:
        module = await load_module(module_name, client, message)
    except Exception as e:
        os.remove(f"./modules/custom_modules/{module_name}.py")
        return await message.edit(format_exc(e))

    await message.edit(
        f"<b>The module <code>{module_name}</code> is loaded!</b>\n\n"
        f"{format_module_help(module_name, False)}"
    )


@Client.on_message(filters.command(["unloadmod", "ulm"], prefix) & filters.me)
async def unload_mods(client: Client, message: Message):
    if len(message.command) <= 1:
        return await message.edit("<b>Specify module to unload</b>")

    module_name = message.command[1].lower()

    if os.path.exists(f"{BASE_PATH}/modules/custom_modules/{module_name}.py"):
        try:
            await unload_module(module_name, client)
        except Exception as e:
            return await message.edit(format_exc(e))

        os.remove(f"{BASE_PATH}/modules/custom_modules/{module_name}.py")
        await message.edit(
            f"<b>The module <code>{module_name}</code> removed!</b>"
        )
    elif os.path.exists(f"{BASE_PATH}/modules/{module_name}.py"):
        await message.edit(
            "<b>It is forbidden to remove built-in modules, it will disrupt the updater</b>"
        )
    else:
        await message.edit(
            f"<b>Module <code>{module_name}</code> is not found</b>"
        )


@Client.on_message(filters.command(["loadallmods"], prefix) & filters.me)
async def load_all_mods(client: Client, message: Message):
    await message.edit("<b>Fetching info...</b>")

    if not os.path.exists(f"{BASE_PATH}/modules/custom_modules"):
        os.mkdir(f"{BASE_PATH}/modules/custom_modules")

    modules_list = requests.get(
        "https://api.github.com/repos/Dragon-Userbot/custom_modules/contents/",
        params={"ref": modules_repo_branch},
    ).json()

    new_modules = {}
    for module_info in modules_list:
        if not module_info["name"].endswith(".py"):
            continue
        if os.path.exists(
            f'{BASE_PATH}/modules/custom_modules/{module_info["name"]}'
        ):
            continue
        new_modules[module_info["name"][:-3]] = module_info["download_url"]
    if not new_modules:
        return await message.edit("<b>All modules already loaded</b>")

    await message.edit(
        f"<b>Loading new modules (it may take a lot of time): "
        f'{" ".join(new_modules.keys())}</b>'
    )

    for module_name, url in new_modules.items():
        with open(f"./modules/custom_modules/{module_name}.py", "wb") as f:
            f.write(requests.get(url).content)

        await load_module(module_name, client)

    await message.edit(
        f'<b>Successfully loaded new modules: {" ".join(new_modules.keys())}</b>'
    )


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
            "https://raw.githubusercontent.com/Dragon-Userbot/"
            f"custom_modules/{modules_repo_branch}/{module_name}"
        )
        if not resp.ok:
            modules_installed.remove(module_name)
            continue

        with open(f"./modules/custom_modules/{module_name}", "wb") as f:
            f.write(resp.content)

        # Unloading and loading modules manually will take a lot of time
        # Restart will do this work faster

    await message.edit(
        f"<b>Successfully updated {len(modules_installed)} modules</b>"
    )

    restart()


modules_help["loader"] = {
    "loadmod [module_name]*": (
        "Download module.\n"
        "Only modules from the official custom_modules repository are supported"
    ),
    "unloadmod [module_name]*": "Delete module",
    "loadallmods": "Load all custom modules (use it at your own risk)",
    "updateallmods": "Update all loaded custom modules",
}
