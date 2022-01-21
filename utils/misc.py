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

import configparser
import os
import sys
from sys import version_info
from .db import db


class ModulesHelpDict(dict):
    def append(self, obj: dict):
        # convert help from old to new type
        module_name = list(obj.keys())[0]
        cmds = obj[module_name]
        commands = {}
        for cmd in cmds:
            cmd_name = list(cmd.keys())[0]
            cmd_desc = cmd[cmd_name]
            commands[cmd_name] = cmd_desc
        self[module_name] = commands


modules_help = ModulesHelpDict()
requirements_list = []

python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
userbot_version = "2.0.3"

config_path = os.path.join(sys.path[0], "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

pr = db.get("core.main", "prefix")
if pr is None:
    db.set("core.main", "prefix", ".")
    prefix = "."
else:
    prefix = pr
