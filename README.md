# aRadio
Raspberry Pi

winscp file and folder exclusion:

SingletonCookie
SingletonLock
SingletonSocket
*.pyc


.vscode-server/
.git/
__pycache__/

alsamixer
speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav

sudo nano /etc/pulse/daemon.conf
enable-shm = no
default-fragments = 5
default-fragment-size-msec = 2

sudo nano /home/pi/.asoundrc



sudo apt-get install -y mpg123
mpg123 http://ice1.somafm.com/u80s-128-mp3
