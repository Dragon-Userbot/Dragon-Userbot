apt-get update && apt-get upgrade -y
apt install python3-pip git wget -y
apt-get install python3 -y
pkg install python -y
pip3 install wheel
pip3 install --upgrade pip
pkg install python libjpeg-turbo libcrypt ndk-sysroot clang zlib -y
LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" pip install --upgrade wheel pillow
apt install ffmpeg -y
pip3 install -r requirements.txt

echo ====================================
read -p 'Enter your db_url: ' uservar
echo ====================================

python3 install.py $uservar

