#!/bin/bash
if [[ $UID != 0 ]] && ! command -v termux-setup-storage; then
  echo Please run this script as root
  exit 1
fi

apt update -y
apt install python3 python3-pip git clang ffmpeg wget gnupg -y
if command -v termux-setup-storage; then
  apt install libjpeg-turbo libcrypt ndk-sysroot zlib -y
fi

python3 -m pip install -U pip
LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" python3 -m pip install -U wheel pillow

git clone https://github.com/Dragon-Userbot/Dragon-Userbot || exit 2
cd Dragon-Userbot
python3 -m pip install -U -r requirements.txt

echo
echo "Enter API_ID and API_HASH"
echo "You can get it here -> https://my.telegram.org/apps"
echo "Leave empty to use defaults"
read -r -p "API_ID > " api_id
if [[ $api_id = "" ]]; then
  api_id=2040
  api_hash=b18441a1ff607e10a989891a5462e627
else
  read -r -p "API_HASH > " api_hash
fi

echo
if command -v termux-setup-storage; then
  echo "Choose database type:"
  echo "[1] MongoDB (your url)"
  echo "[2] Sqlite"
  read -r -p "[1] > " db_type
  if [[ $db_type = 2 ]]; then
    db_type=3
  fi
else
  echo "Choose database type:"
  echo "[1] MongoDB db_url"
  echo "[2] MongoDB localhost"
  echo "[3] Sqlite (default)"
  read -r -p "> " db_type
fi

echo
case $db_type in
  1)
    echo "Please enter db_url"
    echo "You can get it here -> https://telegra.ph/How-to-get-Mongodb-URL-and-login-in-telegram-08-01"
    read -r -p "> " db_url
    db_name=Dragon_Userbot
    ;;
  2)
    if ! command -v mongo && ! command -v mongosh; then
      wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
      source /etc/os-release
      echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu ${UBUNTU_CODENAME}/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
      apt update
      apt install mongodb -y
      systemctl daemon-reload
      systemctl start mongod
      systemctl enable mongod
    fi
    db_url=mongodb://localhost:27017
    db_name=Dragon_Userbot
    ;;
  *)
    db_name=db.sqlite3
    ;;
esac

if [[ $db_type = 1 ]] || [[ $db_type = 2 ]]; then
  db_type_named=mongodb
else
  db_type_named=sqlite3
fi

cat > .env << EOL
API_ID=${api_id}
API_HASH=${api_hash}

# sqlite/sqlite3 or mongo/mongodb
DATABASE_TYPE=${db_type_named}
# file name for sqlite3, database name for mongodb
DATABASE_NAME=${db_name}

# only for mongodb
DATABASE_URL=${db_url}
EOL

su -c "python3 install.py" $SUDO_USER

if ! command -v termux-setup-storage; then
  echo "Choose installation type:"
  echo "[1] PM2"
  echo "[2] Systemd service"
  echo "[3] Custom (default)"
  read -r -p "> " install_type
else
  install_type=3
fi

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
    echo
    ;;
  *)
    echo
    echo "============================"
    echo "Great! Dragon-Userbot installed successfully!"
    echo "Installation type: Custom"
    echo "Start with: \"python3 main.py\""
    echo "============================"
    echo
    ;;
esac

chown -R $SUDO_USER .