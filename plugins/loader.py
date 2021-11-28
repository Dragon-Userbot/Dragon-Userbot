from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from .utils.scripts import restart
import requests
import os
import hashlib


@Client.on_message(filters.command(["modhash", "mh"], prefix) & filters.me)
async def get_mod_hash(client: Client, message: Message):
    if len(message.command) == 1:
        return
    url = message.command[1]
    resp = requests.get(url)
    if not resp.ok:
        await message.edit(
            f"<b>Troubleshooting with downloading module <code>{url}</code></b>"
        )
        return
    await message.edit(
        f"<b>Module hash: <code>{hashlib.sha256(resp.content).hexdigest()}</code></b>"
    )


@Client.on_message(filters.command(["loadmod", "lm"], prefix) & filters.me)
async def load_mods(client: Client, message: Message):
    if len(message.command) == 1:
        return
    url = message.command[1]

    async def download_mod(content=None):
        if not os.path.exists(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules"):
            os.mkdir(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules")
        code = requests.get(url) if content is None else content
        if not code.ok:
            await message.edit(
                f'<b>Can\'t find module <code>{url.split("/")[-1].split(".")[0]}</code></b>'
            )
            return
        with open(f'./plugins/custom_modules/{url.split("/")[-1]}', "wb") as mod:
            mod.write(code.content)
        await message.edit(
            f'<b>The module <code>{url.split("/")[-1].split(".")[0]}</code> is loaded!</b>'
        )
        await restart()

    if (
        "/".join(url.split("/")[:6])
        == "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main"
    ):
        await download_mod()
    elif "/" not in url and "." not in url:
        url = f"https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/{url}.py"
        await download_mod()
    else:
        resp = requests.get(url)
        if not resp.ok:
            await message.edit(
                f"<b>Troubleshooting with downloading module <code>{url}</code></b>"
            )
            return
        hashes = requests.get(
            "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/modules_hashes.txt"
        ).text
        if hashlib.sha256(resp.content).hexdigest() in hashes:
            await download_mod(resp)
        else:
            await message.edit(
                "<b>Only <a href=https://github.com/Dragon-Userbot/custom_modules/main/modules_hashes.txt>verified"
                "</a> modules or from the official <a href=https://github.com/Dragon-Userbot/custom_modules>"
                "custom_modules</a> repository are supported!</b>",
                disable_web_page_preview=True,
            )


@Client.on_message(filters.command(["unloadmod", "ulm"], prefix) & filters.me)
async def unload_mods(client: Client, message: Message):
    if len(message.command) > 1:
        mod = message.command[1]
        if (
            "/".join(mod.split("/")[:6])
            == "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main"
        ):
            mod = "/".join(mod.split("/")[6:]).split(".")[0]

        if os.path.exists(
            f"{os.path.abspath(os.getcwd())}/plugins/custom_modules/{mod}.py"
        ):
            os.remove(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules/{mod}.py")
            await message.edit(f"<b>The module <code>{mod}</code> removed!</b>")
            await restart()

        elif os.path.exists(f"{os.path.abspath(os.getcwd())}/plugins/{mod}.py"):
            await message.edit(
                f"<b>It is forbidden to remove built-in modules, it will disrupt the updater</b>"
            )

        else:
            await message.edit(f"<b>Module <code>{mod}</code> not found</b>")


@Client.on_message(filters.command(["loadallmods"], prefix) & filters.me)
async def load_all_mods(clent: Client, message: Message):
    await message.edit("<b>Fetching info...</b>")
    if not os.path.exists(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules"):
        os.mkdir(f"{os.path.abspath(os.getcwd())}/plugins/custom_modules")
    modules_list = requests.get(
        "https://api.github.com/repos/Dragon-Userbot/custom_modules/contents/"
    ).json()
    new_modules = {}
    for module_info in modules_list:
        if not module_info["name"].endswith(".py"):
            continue
        if os.path.exists(
            f'{os.path.abspath(os.getcwd())}/plugins/custom_modules/{module_info["name"]}'
        ):
            continue
        new_modules.update({module_info["name"][:-3]: module_info["download_url"]})
    if len(new_modules) == 0:
        return await message.edit("<b>All modules already loaded</b>")
    await message.edit(f'<b>Loading new modules: {" ".join(new_modules.keys())}</b>')
    for name, url in new_modules.items():
        with open(f"./plugins/custom_modules/{name}.py", "wb") as f:
            f.write(requests.get(url).content)
    await message.edit(
        f'<b>Successfully loaded new modules: {" ".join(new_modules.keys())}</b>'
    )
    await restart()


modules_help.append(
    {
        "loader": [
            {
                "loadmod [link]*": "Download module\nOnly modules from the official custom_modules repository and proven modules whose hashes are in modules_hashes.txt are supported"
            },
            {"unloadmod [module_name]*": "Delete module"},
            {"modhash [link]*": "Get module hash by link"},
            {"loadallmods": "Load all custom modules (use it at your own risk)"},
        ]
    }
)
