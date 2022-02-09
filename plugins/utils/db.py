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

import dns.resolver
import pymongo as md

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]


class DataBase:
    def __init__(self):
        config_path = os.path.join(sys.path[0], "config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)
        db_url = config.get("pyrogram", "db_url")
        try:
            db_name = config.get("db", "db_name")
        except:
            try:
                config.add_section("db")
            except:
                pass
            config.set("db", "db_name", "Dragon_Userbot")
            with open(config_path, "w") as f:
                config.write(f)
            os.system("python3 main.py")
        self._DB = md.MongoClient(db_url)[db_name]

    def set(self, module: str, variable: str, value):
        modcollection = self._DB[module]
        doc = modcollection.find_one({"var": variable})
        if doc is None:
            modcollection.insert_one({"var": variable, "val": value})
        else:
            modcollection.replace_one(doc, {"var": variable, "val": value})
        return True

    def get(self, module: str, variable: str, expected_value=None):
        modcollection = self._DB[module]
        doc = modcollection.find_one({"var": variable})
        if doc is None:
            return expected_value
        else:
            return doc["val"]

    def get_collection(self, module: str):
        modcollection = self._DB[module]
        return [{_["var"]: _["val"]} for _ in modcollection.find()]

    def remove(self, module: str, variable: str):
        modcollection = self._DB[module]
        doc = modcollection.find_one({"var": variable})
        if doc != None:
            modcollection.delete_one(doc)
            return True
        else:
            return False


db = DataBase()
