from pyrogram import Client, idle
import sys
from plugins.utils.db import db
from pyrogram.raw.functions.account import GetAuthorizations

app = Client("my_account")

if __name__ == "__main__":
    app.start()
    if len(sys.argv) == 4:
        try:
            restart_type = sys.argv[3]
            if restart_type == "1":
                text = "<code>Update process completed!</code>"
            else:
                text = "<code>Restart completed!</code>"
            app.send_message(
                chat_id=sys.argv[1], text=text, reply_to_message_id=int(sys.argv[2])
            )
        except:
            app.send_message(chat_id=sys.argv[1], text=text)
    auths = app.send(GetAuthorizations())["authorizations"]
    auth_hashes = [auth["hash"] for auth in auths]
    db.set("core.sessionkiller", "auths_hashes", auth_hashes)
    idle()
