# aRadio
Raspberry Pi

## hints

### winscp
winscp file and folder exclusion:

SingletonCookie
SingletonLock
SingletonSocket
*.pyc


.vscode-server/
.git/
__pycache__/

### alsamixer
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

### sound
https://www.tinkerboy.xyz/raspberry-pi-test-sound-output/
check (usb)sound devices:

cat /proc/asound/modules
  0 snd_bcm2835
  1 snd_usb_audio
cat /proc/asound/cards
  0 [b1             ]: bcm2835_hdmi - bcm2835 HDMI 1
                      bcm2835 HDMI 1
  1 [Headphones     ]: bcm2835_headpho - bcm2835 Headphones
                      bcm2835 Headphones
  
  the first number ist the device number used as "N" here:
speaker-test -c2 -twav -l7 -D plughw:N,0
  similar in omxplayer: 
omxplayer example.mp3 -o alsa:hw:N,0

https://support.thepihut.com/hc/en-us/articles/360010336738-No-sound-output-with-my-Raspberry-Pi-4
https://projects-raspberry.com/getting-audio-out-working-on-the-raspberry-pi/
https://www.instructables.com/Test-Sound-Card-and-Speakers-in-Raspberry-Pi/

sudo apt update && sudo apt install pavucontrol 

try:
sudo sed -i 's/vc4-fkms-v3d/vc4-kms-v3d/g' /boot/config.txt
or:
sudo sed -i 's/vc4-kms-v3d/vc4-fkms-v3d/g' /boot/config.txt

### omxplayer
omxplayer -o local /home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4"
omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
omxplayer -o local '/home/pi/aRadio/theRadio/bImages/Electronics_At_Work_1943_Part_3.mp4' --win '0 0 248 180' --no-osd
omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '0 0 800 480'
omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 992 720'
omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 496 360'
omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 248 180'
omxplayer -o local 'https://liveradio.swr.de/sw282p3/swr1bw/play.mp3'
omxplayer -o alsa:hw:0,0 'https://liveradio.swr.de/sw282p3/swr1bw/play.mp3'
omxplayer -o hdmi 'https://youtu.be/YtPSa4LTWgo'
omxplayer -o alsa:hw:0,0 'https://youtu.be/YtPSa4LTWgo'

if missing, do "update", if thats failing, do "sudo apt full-upgrade" and "sudo apt dist-upgrade" and "sudo rpi-update"
sudo apt update && sudo apt full-upgrade && sudo apt dist-upgrade && sudo rpi-update
sudo apt update && sudo apt install --reinstall omxplayer -y
sudo apt update && sudo apt install --reinstall vlc -y
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E
wget https://archive.raspbian.org/raspbian.public.key -O - | sudo apt-key add -


https://www.cyberrypi.de/blogs/raspberry-pi-blog/informationen-zum-omxplayer-befehlszeilen-mediaplayer

#### maybe, to get omxplayer back:
sudo su
cd /usr/lib/arm-linux-gnueabihf
ln -s libmmal_core.so.0 libmmal_core.so
ln -s libmmal_util.so.0 libmmal_util.so
ln -s libmmal_vc_client.so.0 libmmal_vc_client.so
ln -s libbcm_host.so.0 libbcm_host.so
ln -s libvcsm.so.0 libvcsm.so
ln -s libvchiq_arm.so.0 libvchiq_arm.so
ln -s libvcos.so.0 libvcos.so
curl -sSfLO 'https://raw.githubusercontent.com/raspberrypi/firmware/master/opt/vc/lib/libbrcmEGL.so'
curl -sSfLO 'https://raw.githubusercontent.com/raspberrypi/firmware/master/opt/vc/lib/libbrcmGLESv2.so'
curl -sSfLO 'https://raw.githubusercontent.com/raspberrypi/firmware/master/opt/vc/lib/libopenmaxil.so'



### display

 DISPLAY=:0 /usr/bin/lxterminal -e mplayer '/mnt/c/Users/janka_cg1/Dropbox/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
 DISPLAY=:0 /usr/bin/lxterm -e mplayer '/mnt/c/Users/janka_cg1/Dropbox/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
 DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
 DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/Music/Asaf Avidan - One Day Live @ Sziget 2015.mp3'

### boot
smsc95xx.turbo_mode=N dwc_otg.dma_enable=1 dwc_otg.dma_burst_size=256 dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=e64496a0-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait consoleblank=0
