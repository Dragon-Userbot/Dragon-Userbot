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

import json
import threading
import dns.resolver
import pymongo
import sqlite3
from utils import config

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]


class Database:
    def get(self, module: str, variable: str, default=None):
        """Get value from database"""
        raise NotImplementedError

    def set(self, module: str, variable: str, value):
        """Set key in database"""
        raise NotImplementedError

    def remove(self, module: str, variable: str):
        """Remove key from database"""
        raise NotImplementedError

    def get_collection(self, module: str) -> dict:
        """Get database for selected module"""
        raise NotImplementedError

    def close(self):
        """Close the database"""
        raise NotImplementedError


class MongoDatabase(Database):
    def __init__(self, url, name):
        self._client = pymongo.MongoClient(url)
        self._database = self._client[name]

    def set(self, module: str, variable: str, value):
        self._database[module].replace_one(
            {"var": variable}, {"var": variable, "val": value}, upsert=True
        )

    def get(self, module: str, variable: str, expected_value=None):
        doc = self._database[module].find_one({"var": variable})
        return expected_value if doc is None else doc["val"]

    def get_collection(self, module: str):
        return {
            item["var"]: item["val"] for item in self._database[module].find()
        }

    def remove(self, module: str, variable: str):
        self._database[module].delete_one({"var": variable})

    def close(self):
        self._client.close()


class SqliteDatabase(Database):
    def __init__(self, file):
        self._conn = sqlite3.connect(file, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        self._lock = threading.Lock()

    @staticmethod
    def _parse_row(row: sqlite3.Row):
        if row["type"] == "bool":
            return row["val"] == "1"
        elif row["type"] == "int":
            return int(row["val"])
        elif row["type"] == "str":
            return row["val"]
        else:
            return json.loads(row["val"])

    def _execute(self, module: str, *args, **kwargs) -> sqlite3.Cursor:
        self._lock.acquire()
        try:
            return self._cursor.execute(*args, **kwargs)
        except sqlite3.OperationalError as e:
            if str(e).startswith("no such table"):
                sql = f"""
                CREATE TABLE IF NOT EXISTS '{module}' (
                var TEXT UNIQUE NOT NULL,
                val TEXT NOT NULL,
                type TEXT NOT NULL
                )
                """
                self._cursor.execute(sql)
                self._conn.commit()
                return self._cursor.execute(*args, **kwargs)
            raise e from None
        finally:
            self._lock.release()

    def get(self, module: str, variable: str, default=None):
        sql = f"SELECT * FROM '{module}' WHERE var=:var"
        cur = self._execute(module, sql, {"tabl": module, "var": variable})

        row = cur.fetchone()
        if row is None:
            return default
        else:
            return self._parse_row(row)

    def set(self, module: str, variable: str, value) -> bool:
        sql = f"""
        INSERT INTO '{module}' VALUES ( :var, :val, :type )
        ON CONFLICT (var) DO
        UPDATE SET val=:val, type=:type WHERE var=:var
        """

        if isinstance(value, bool):
            val = "1" if value else "0"
            typ = "bool"
        elif isinstance(value, str):
            val = value
            typ = "str"
        elif isinstance(value, int):
            val = str(value)
            typ = "int"
        else:
            val = json.dumps(value)
            typ = "json"

        self._execute(module, sql, {"var": variable, "val": val, "type": typ})
        self._conn.commit()

        return True

    def remove(self, module: str, variable: str):
        sql = f"DELETE FROM '{module}' WHERE var=:var"
        self._execute(module, sql, {"var": variable})
        self._conn.commit()

    def get_collection(self, module: str) -> dict:
        sql = f"SELECT * FROM '{module}'"
        cur = self._execute(module, sql)

        collection = {}
        for row in cur:
            collection[row["var"]] = self._parse_row(row)

        return collection

    def close(self):
        self._conn.commit()
        self._conn.close()


if config.db_type in ["mongo", "mongodb"]:
    db = MongoDatabase(config.db_url, config.db_name)
else:
    db = SqliteDatabase(config.db_name)
