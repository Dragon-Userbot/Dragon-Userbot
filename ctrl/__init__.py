from pyrogram import Client
from utils.misc import gitrepo, userbot_version
from utils import config


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

app.start()

ok = app.get_me()
my_username = ok.username
my_id = ok.id
my_first_name = ok.first_name
my_last_name = ok.last_name

idle()
