if ! command -v termux-setup-storage; then
  echo This script can be executed only on Termux
  exit 1
fi

termux-wake-lock

apt update -y
apt install python3 git clang ffmpeg wget libjpeg-turbo libcrypt ndk-sysroot zlib -y || exit 2

python3 -m pip install -U pip
LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" pip3 install --upgrade wheel pillow

git clone https://github.com/Dragon-Userbot/Dragon-Userbot || exit 2
cd Dragon-Userbot || exit 2
git checkout fs_rewrite_imports
python3 -m pip install -U -r requirements.txt || exit 2

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

echo "Choose database type:"
echo "[1] MongoDB (your url)"
echo "[2] Sqlite"
read -r -p "> " db_type

if [[ $db_type = 1 ]]; then
  echo "Please enter db_url"
  echo "You can get it here -> https://telegra.ph/How-to-get-Mongodb-URL-and-login-in-telegram-08-01"
  read -r -p "> " db_url
  db_name=Dragon_Userbot
  db_type=mongodb
else
  db_name=db.sqlite3
  db_type=sqlite3
fi

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

python3 install.py 3 || exit 3

echo
echo "============================"
echo "Great! Dragon-Userbot installed successfully!"
echo "Start with: \"python3 main.py\""
echo "============================"