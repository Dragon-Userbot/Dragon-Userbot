from sys import version_info
import motor.motor_asyncio
import configparser
import sys
import os


modules_help = {}
requirements_list = []

github = '<a href=https://github.com/Dragon-Userbot/Dragon-Userbot> github</a>'
license = '<a href=https://github.com/Dragon-Userbot/Dragon-Userbot/blob/master/LICENSE> GNU General Public License v3.0</a>'
copyright = '© <a href=https://github.com/Dragon-Userbot>Dragon-Userbot company</a>, 2021'
python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
version = '1.1.4'


config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
db_url = config.get("pyrogram", "db_url")
connectDB = motor.motor_asyncio.AsyncIOMotorClient(db_url)
createDB = connectDB.Dragon_Userbot


def get_prefix():
    prefix = config.get("prefix", "prefix")
    return prefix
        

try:
    prefix = get_prefix()

except Exception as e:
    config.add_section("prefix")
    config.set('prefix', 'prefix', '.')
    with open(config_path, "w") as config_file:
        config.write(config_file)
    prefix = '.'
