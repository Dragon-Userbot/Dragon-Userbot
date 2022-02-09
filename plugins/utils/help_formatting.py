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

import re

from .utils import prefix


def help_formatting(module_help, help_type, module_name):
    if help_type == "all_mods":
        return f"• <b>{module_help.split(':')[0].strip()}: </b> <code>{module_help.split(':')[1].strip()}</code>\n"

    elif help_type == "one_mod":
        s = f"<b>Help for |{module_name}|\nUsage:</b>\n"
        try:
            for i in module_help.split(","):
                command, description = i.split("-", maxsplit=1)
                command = re.sub(r"^\s+|\s+$", "", command)
                description = re.sub(r"^\s+|\s+$", "", description)
                s += f"<code>{prefix}{command}</code>\n<b>[{description}]</b>\n"
            return s
        except IndexError:
            return module_help
