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

default-fragments = 5
default-fragment-size-msec = 25


sudo nano /home/pi/.asoundrc



sudo apt-get install -y mpg123
mpg123 http://ice1.somafm.com/u80s-128-mp3
mpg123 http://ice1.somafm.com/seventies-128-mp3
mpg123 http://ice1.somafm.com/thistle-128-mp3

cat /proc/asound/cards

 0 [b1             ]: bcm2835_hdmi - bcm2835 HDMI 1
                      bcm2835 HDMI 1
 1 [Headphones     ]: bcm2835_headpho - bcm2835 Headphones
                      bcm2835 Headphones



smsc95xx.turbo_mode=N dwc_otg.dma_enable=1 dwc_otg.dma_burst_size=256 dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=e64496a0-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait consoleblank=0
