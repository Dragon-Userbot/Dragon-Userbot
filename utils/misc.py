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

from sys import version_info
from .db import db
from git import Repo


class ModulesHelp(dict):
    def __setitem__(self, key, value):
        return super().__setitem__(str(key).lower(), value)

    def __getitem__(self, item):
        return super().__getitem__(str(item).lower())


modules_help = ModulesHelp()
requirements_list = []

python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"

prefix = db.get("core.main", "prefix", ".")

gitrepo = Repo(".")
commits_since_tag = list(gitrepo.iter_commits(f"{gitrepo.tags[-1].name}..HEAD"))
userbot_version = f"4.0.{len(commits_since_tag)}"
