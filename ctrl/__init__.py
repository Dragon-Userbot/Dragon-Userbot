import sys
import asyncio
import logging
import platform
from pytgcalls import PyTgCalls
from pyrogram import Client
from utils import config
from utils.misc import gitrepo, userbot_version
from logging import DEBUG, INFO, basicConfig, getLogger

LOG_FILE_NAME = "logs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)


logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("py-tgcalls").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.syncer").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)
logs = logging.getLogger(__name__)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


try:
    app = Client(
        name="my_account",
        api_id=config.api_id,
        api_hash=config.api_hash,
        session_string=config.session_string,
        hide_password=True,
        workdir=script_path,
        app_version=userbot_version,
        device_model=f"CtrlUB @ {gitrepo.head.commit.hexsha[:7]}",
        system_version=platform.version() + " " + platform.machine(),
        sleep_threshold=30,
        test_mode=config.test_server,
        in_memory=True
    )
    call = PyTgCalls(app)
except Exception as e:
    logs.info(f"{e}")
    sys.exit()

app.start()
calls = call.start
