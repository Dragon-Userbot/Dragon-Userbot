apt-get update
apt install python3-pip git wget
pip3 install wheel
pip3 install --upgrade pip
pkg install python libjpeg-turbo libcrypt ndk-sysroot clang zlib
LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" pip install --upgrade wheel pillow
apt update
apt install ffmpeg
pip3 install -r requirements.txt

echo ====================================
read -p 'Enter your db_url: ' uservar
echo ====================================

python3 add_dburl.py $uservar

python3 main.py