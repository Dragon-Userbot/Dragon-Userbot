from sys import prefix, version_info
import motor.motor_asyncio
import configparser
import sys
import os
from .db import db
import asyncio

modules_help = {}
requirements_list = []

github = '<a href=https://github.com/Dragon-Userbot/Dragon-Userbot> github</a>'
license = (
    '<a href=https://github.com/Dragon-Userbot/Dragon-Userbot/blob/master/LICENSE> GNU'
    ' General Public License v3.0</a>'
)
copyright = (
    '© <a href=https://github.com/Dragon-Userbot>Dragon-Userbot company</a>, 2021'
)
python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
version = '1.2.2.1'


config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

pr = db.get('core.main', 'prefix')
if pr is None:
    db.set('core.main', 'prefix', '.')
    prefix = '.'
else:
    prefix = pr

try:
    sessionkiller_enabled = config.get("sessionkiller", "enabled")
except:
    config.add_section('sessionkiller')
    config.set('sessionkiller', 'enabled', '0')
    with open(config_path, 'w') as config_file:
        config.write(config_file)
    sessionkiller_enabled = '0'

if sessionkiller_enabled in ['0', 'false', 'no', 'disabled']:
    sessionkiller_enabled = False
else:
    sessionkiller_enabled = True
