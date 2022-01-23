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

from pyrogram import Client, filters
from pyrogram.types import Message

from covid import Covid
from utils.misc import modules_help, prefix
from utils.misc import requirements_list


@Client.on_message(filters.command("covid", prefix) & filters.me)
async def covid_local(_, message: Message):
    region = " ".join(message.command[1:])
    await message.edit("<b>Data retrieval...</b>")
    covid = Covid(source="worldometers")
    try:
        local_status = covid.get_status_by_country_name(region)
        await message.edit(
            "<b>=======🦠 COVID-19 STATUS 🦠=======</b>\n"
            + f"<b>Region</b>: <code>{local_status['country']}</code>\n"
            + "<b>====================================</b>\n"
            + f"<b>🤧 New cases</b>: <code>{local_status['new_cases']}</code>\n"
            + f"<b>😷 New deaths</b>: <code>{local_status['new_deaths']}</code>\n"
            + "<b>====================================</b>\n"
            + f"<b>😷 Сonfirmed</b>: <code>{local_status['confirmed']}</code>\n"
            + f"<b>❗️ Active:</b> <code>{local_status['active']}</code>\n"
            + f"<b>⚠️ Critical</b>: <code>{local_status['critical']}</code>\n"
            + f"<b>💀 Deaths</b>: <code>{local_status['deaths']}</code>\n"
            + f"<b>🚑 Recovered</b>: <code>{local_status['recovered']}</code>\n"
        )
    except ValueError:
        await message.edit(f"<b>There is no region called {region}</b>")


@Client.on_message(filters.command("regions", prefix) & filters.me)
async def regions_cmd(_, message: Message):
    countries = ""
    await message.edit("<b>Data retrieval...</b>")
    covid = Covid(source="worldometers")
    for region in covid.list_countries():
        countries += f"<code>{region}</code>\n"
    await message.edit(countries)


modules_help["covidinfo"] = {
    "covid [region]*": "COVID-19 status by region",
    "regions": "Available regions</i>\n\n"
    "<b>Worldometer.info statistics are used</b><i>",
}

requirements_list.append("covid")
