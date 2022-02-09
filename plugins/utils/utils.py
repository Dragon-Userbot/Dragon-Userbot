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

modules_help = []
requirements_list = []

github = "<a href=https://github.com/Dragon-Userbot/Dragon-Userbot> github</a>"
license = (
    "<a href=https://github.com/Dragon-Userbot/Dragon-Userbot/blob/master/LICENSE> GNU"
    " General Public License v3.0</a>"
)
copyright = (
    "© <a href=https://github.com/Dragon-Userbot>Dragon-Userbot company</a>, 2021"
)
python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
version = "2.0.3"

config_path = os.path.join(sys.path[0], "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

pr = db.get("core.main", "prefix")
if pr is None:
    db.set("core.main", "prefix", ".")
    prefix = "."
else:
    prefix = pr
