import configparser
import os
import sys


if len(sys.argv) == 2:
    arg = sys.argv[1]
    config_path = os.path.join(sys.path[0], 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)

    config.set('pyrogram', 'db_url', arg)
    with open(config_path, "w") as config_file:
        config.write(config_file)

