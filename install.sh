#!/bin/bash
if command -v termux-setup-storage; then
  echo For termux, please use https://raw.githubusercontent.com/Dragon-Userbot/Dragon-Userbot/main/termux-install.sh
  exit 1
fi

if [[ $UID != 0 ]]; then
  echo Please run this script as root
  exit 1
fi

apt update -y
apt install python3 python3-pip git ffmpeg wget gnupg -y || exit 2

su -c "python3 -m pip install -U pip" $SUDO_USER
su -c "python3 -m pip install -U wheel pillow" $SUDO_USER

if [[ -d "Dragon-Userbot" ]]; then
  cd Dragon-Userbot
elif [[ -f ".env.dist" ]] && [[ -f "main.py" ]] && [[ -d "modules" ]]; then
  :
else
  git clone https://github.com/Dragon-Userbot/Dragon-Userbot || exit 2
  cd Dragon-Userbot || exit 2
fi

if [[ -f ".env" ]] && [[ -f "my_account.session" ]]; then
  echo "It seems that Dragon-Userbot is already installed. Exiting..."
  exit
fi

su -c "python3 -m pip install -U -r requirements.txt" $SUDO_USER || exit 2

echo
echo "Enter API_ID and API_HASH"
echo "You can get it here -> https://my.telegram.org/apps"
echo "Leave empty to use defaults (please note that default keys significantly increases your ban chances)"
read -r -p "API_ID > " api_id

if [[ $api_id = "" ]]; then
  api_id="2040"
  api_hash="b18441a1ff607e10a989891a5462e627"
else
  read -r -p "API_HASH > " api_hash
fi

echo
echo "Choose database type:"
echo "[1] MongoDB db_url"
echo "[2] MongoDB localhost"
echo "[3] Sqlite (default)"
read -r -p "> " db_type

echo
case $db_type in
  1)
    echo "Please enter db_url"
    echo "You can get it here -> https://telegra.ph/How-to-get-Mongodb-URL-and-login-in-telegram-08-01"
    read -r -p "> " db_url
    db_name=Dragon_Userbot
    db_type=mongodb
    ;;
  2)
    if systemctl status mongodb; then
      wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
      source /etc/os-release
      echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu ${UBUNTU_CODENAME}/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
      apt update
      apt install mongodb -y
      systemctl daemon-reload
      systemctl enable mongodb
    fi
    systemctl start mongodb

    db_url=mongodb://localhost:27017
    db_name=Dragon_Userbot
    db_type=mongodb
    ;;
  *)
    db_name=db.sqlite3
    db_type=sqlite3
    ;;
esac

cat > .env << EOL
API_ID=${api_id}
API_HASH=${api_hash}

# sqlite/sqlite3 or mongo/mongodb
DATABASE_TYPE=${db_type}
# file name for sqlite3, database name for mongodb
DATABASE_NAME=${db_name}

# only for mongodb
DATABASE_URL=${db_url}
EOL

chown -R $SUDO_USER:$SUDO_USER .

echo
echo "Choose installation type:"
echo "[1] PM2"
echo "[2] Systemd service"
echo "[3] Custom (default)"
read -r -p "> " install_type

su -c "python3 install.py ${install_type}" $SUDO_USER || exit 3

case $install_type in
  1)
    if ! command -v pm2; then
      curl -fsSL https://deb.nodesource.com/setup_17.x | bash
      apt install nodejs -y
      npm install pm2 -g
      su -c "pm2 startup" $SUDO_USER
      env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u $SUDO_USER --hp /home/$SUDO_USER
    fi
    su -c "pm2 start main.py --name dragon --interpreter python3" $SUDO_USER
    su -c "pm2 save" $SUDO_USER

    echo
    echo "============================"
    echo "Great! Dragon-Userbot installed successfully and running now!"
    echo "Installation type: PM2"
    echo "Start with: \"pm2 start dragon\""
    echo "Stop with: \"pm2 stop dragon\""
    echo "Process name: dragon"
    echo "============================"
    ;;
  2)
    cat > /etc/systemd/system/dragon.service << EOL
[Unit]
Description=Service for Dragon Userbot

[Service]
Type=simple
ExecStart=$(which python3) ${PWD}/main.py
WorkingDirectory=${PWD}
Restart=always
User=${SUDO_USER}
Group=${SUDO_USER}

[Install]
WantedBy=multi-user.target
EOL
    systemctl daemon-reload
    systemctl start dragon
    systemctl enable dragon

    echo
    echo "============================"
    echo "Great! Dragon-Userbot installed successfully and running now!"
    echo "Installation type: Systemd service"
    echo "Start with: \"sudo systemctl start dragon\""
    echo "Stop with: \"sudo systemctl stop dragon\""
    echo "============================"
    ;;
  *)
    echo
    echo "============================"
    echo "Great! Dragon-Userbot installed successfully!"
    echo "Installation type: Custom"
    echo "Start with: \"python3 main.py\""
    echo "============================"
    ;;
esac

chown -R $SUDO_USER:$SUDO_USER .
