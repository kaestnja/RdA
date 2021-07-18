#!/bin/bash
#version=146

#https://winscp.net/eng/docs/file_mask#basic

#for sdr images from https://www.sdrplay.com/raspberry-pi-images/ :
sudo rm /etc/ssh/ssh_host_*
sudo dpkg-reconfigure openssh-server

#on boot ssh anlegen mit Powershell unter Windows
#------------------------------------------------------------
echo "nothing" > f:\ssh
echo 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
  ssid="SKY"
  scan_ssid=1
  psk="67665741872262767142"
  key_mgmt=WPA-PSK
  priority=1
  id_str="Schoellbronn"
}

network={
  ssid="EARTH"
  scan_ssid=1
  psk="41010552551631877628"
  key_mgmt=WPA-PSK
  priority=2
  id_str="Voelkersbach"
}' > f:\wpa_supplicant.conf
#------------------------------------------------------------
ssh-keyscan -t rsa pi4radio1
ssh -o HostKeyAlias=pi4radio1 pi@pi4radio1
sudo nano ~/.ssh/config
ssh -o StrictHostKeyChecking=no pi@pi4radio1
ssh-keygen -R pi4radio1.fritz.box && ssh -o StrictHostKeyChecking=no pi4radio1.fritz.box echo SSH host key updated.

#ssh-keygen -t rsa -b 2048
ssh-copy-id pi@pi4radio1
ssh-copy-id root@pi4radio1
ssh -i ~/.ssh/id_rsa pi@pi4radio1

#ssh-keygen -t dsa -b 1024
#ssh-copy-id pi@pi4radio1
#ssh-copy-id root@pi4radio1
#ssh -i ~/.ssh/id_dsa pi@pi4radio1
#ssh -i ~/.ssh/id_dsa root@pi4radio1

#plink pi@pi4radio1 -pw toor hostname

#passh -p password ssh pi@pi4radio1

#sudo apt-get install sshpass
#sshpass -p 'toor' ssh pi@pi4radio1
#sshpass -p 'toor' ssh pi@pi4radio1 -p 22
#sshpass -p 'toor' ssh -oStrictHostKeyChecking=no pi@pi4radio1 uptime

#Created symlink /etc/systemd/system/multi-user.target.wants/vncserver-x11-serviced.service → /lib/systemd/system/vncserver-x11-serviced.service.
#sudo ln -s /usr/lib/systemd/system/vncserver-x11-serviced.service /etc/systemd/system/multi-user.target.wants/vncserver-x11-serviced.service
#sudo ln -s /lib/systemd/system/vncserver-x11-serviced.service /etc/systemd/system/multi-user.target.wants/vncserver-x11-serviced.service
#sudo systemctl start vncserver-x11-serviced


plink -ssh pi@raspberrypi -pw raspberry sudo ln -s /lib/systemd/system/vncserver-x11-serviced.service /etc/systemd/system/multi-user.target.wants/vncserver-x11-serviced.service
plink -ssh pi@raspberrypi -pw raspberry sudo systemctl start vncserver-x11-serviced
plink -ssh pi@raspberrypi -pw raspberry sudo reboot

plink -ssh pi@raspberrypi -pw raspberry sudo apt --fix-broken install && sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get clean -y && sudo apt-get dist-upgrade -y && sudo apt-get autoremove -y && sudo apt-get autoclean -y && sudo reboot
plink -ssh pi@raspberrypi -pw raspberry sudo apt-get upgrade -y && sudo apt-get clean -y && sudo apt-get dist-upgrade -y && sudo apt-get autoremove -y && sudo apt-get autoclean -y && sudo reboot


# For this, we need to first set a password for the root user in your pi, which you can do by running:
sudo passwd root
sudo sed -i 's/#PermitRootLogin without-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
# Then we need to enable ssh connections using root, by running :
#sudo nano /etc/ssh/sshd_config
# and adding a line that reads:
#PermitRootLogin yes
# reboot the pi: 
sudo reboot


#ln -s /usr/local/bin/python3.7 /usr/bin/python3
#ln -s /usr/local/bin/pip3.7 /usr/bin/pip3

sudo apt-get install -y python3-rpi.gpio
pip3 install rpi-gpio
sudo pip3 install rpi-gpio
python3 -m pip install --upgrade rpi-gpio 
sudo python3 -m pip install --upgrade rpi-gpio 

sudo cat <<EOF >> $HOME/.bashrc

PATH="${PATH}:$HOME/aRadio/theRadio:$HOME/.local/bin:/usr/local/lib/python3.7:/usr/local/lib/python3.7/dist-packages"
export PATH
PYTHONPATH="${PYTHONPATH}:$HOME/aRadio/theRadio:$HOME/.local/bin:/usr/local/lib/python3.7:/usr/local/lib/python3.7/dist-packages"
export PYTHONPATH

## PiSDR Variables
#DISPLAY=:0.0
#export DISPLAY
#export DISPLAY=0:0
export DISPLAY=:0.0

alias reboot='sudo pkill -f python* && sudo chmod -R 6777 /home && sudo chmod -R 6777 /root && sudo chown -R pi:pi /home/* && sudo reboot'
alias updategit='sudo pkill -SIGKILL -f "python3" > /dev/null 2>&1; cd /home/pi/aRadio && git config credential.helper store >/dev/null && git fetch "https://kaestnja:bc2de507d138f286dc7c9c94f9c41c41a7637b70@github.com/kaestnja/aRadio.git" && git stash && git pull && sudo chown -R pi /home && chmod -R 6777 /home/pi/aRadio && /home/pi/aRadio/GitRepoUpdateTimestamp.sh'
alias update='sudo pkill -f python && sudo chmod -R 6777 /home && sudo chmod -R 6777 /root && sudo chown -R pi:pi /home/ && sudo apt --fix-broken install && sudo apt-get install --fix-missing && sudo apt-get update -y && sudo apt-get upgrade -y --force-yes && sudo apt-get clean -y --force-yes && sudo apt-get dist-upgrade -y --force-yes && sudo apt-get autoremove -y --force-yes && sudo apt-get autoclean -y --force-yes && sudo reboot'
alias swr1bw='omxplayer -o local http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
alias dasding='omxplayer -o local http://swr-dasding-live.cast.addradio.de/swr/dasding/live/mp3/128/stream.mp3'
alias swr3='omxplayer -o local http://swr-swr3-live.cast.addradio.de/swr/swr3/live/mp3/128/stream.mp3'
alias rbb='omxplayer -o local http://rbb-fritz-live.cast.addradio.de/rbb/fritz/live/mp3/128/stream.mp3'
alias mswr1bw='mplayer -quiet -cache 100 http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
alias mdasding='mplayer -quiet -cache 100 http://swr-dasding-live.cast.addradio.de/swr/dasding/live/mp3/128/stream.mp3'
alias mswr3='mplayer -quiet -cache 100 http://swr-swr3-live.cast.addradio.de/swr/swr3/live/mp3/128/stream.mp3'
alias mrbb='mplayer -quiet -cache 100 http://rbb-fritz-live.cast.addradio.de/rbb/fritz/live/mp3/128/stream.mp3'
xset s off > /dev/null 2>&1
EOF

#maybe
#sudo apt-get install -y pi-bluetooth bluetooth bluez blueman

sudo pkill -f python
sudo pkill -f omxplayer
sudo pkill -f chromium
sudo pkill -SIGKILL -f "python3" > /dev/null 2>&1
sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1
sudo pkill -SIGKILL -f "omxplayer.bin" > /dev/null 2>&1

sudo killall -9 omxplayer
sudo killall -9 "omxplayer.bin"

the_hostname=$(hostname)


#sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 379CE192D401AB61
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
sudo apt-key adv --keyserver deb.debian.org --recv-keys 648ACFD622F3D138
#--allow-unauthenticated
sudo apt-key net-update
sudo ldconfig
sudo fc-cache
sudo fc-cache -r

dmesg | grep "Machine model:"
gpio -v
cat /proc/device-tree/model && echo ""
uname -m
cat /proc/cpuinfo | grep 'Revision' | awk '{print $3}'
xdpyinfo | grep dimensions
/opt/vc/bin/tvservice -s
watch 'ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head'
for i in `seq 0 60`; do
  echo `cat /proc/meminfo | grep Active: | sed 's/Active: //g'` >> usage.txt
  sleep 1m
done
for i in `seq 0 60`; do
  echo `cat /proc/meminfo | grep Active: | sed 's/Active: //g'`/`cat /proc/meminfo | grep MemTotal: | sed 's/MemTotal: //g'` >> usage.txt
  sleep 1m
done


#sudo apt-get install -y aptitude
#aptitude why wicd
#sudo apt-get install -y wicd
#sudo apt-get -s remove wicd
#sudo apt-get -s remove python-wicd

sudo apt-get install -y sysstat unclutter watchdog libsdl2-mixer-2.0-0
#sudo nano /etc/default/sysstat
#change ENABLED="false" to ENABLED="true"
if ! sudo grep -q 'ENABLED="true"' "/etc/default/sysstat"; then
  echo "set setting"
  sudo sed -i 's/ENABLED="false"/ENABLED="true"/g' /etc/default/sysstat
fi
#if ! grep -q 'ENABLED="false"' "/etc/default/sysstat"; then
#  sudo sed -i 's/ENABLED="true"/ENABLED="false"/g' /etc/default/sysstat
#fi
sudo service sysstat restart
pidstat -r 2
pidstat -t -p 4164 2 3
pidstat -rh 6 10
pidstat -t -G python
#https://linuxhint.com/sar_linux_tutorial/
sar -n DEV
sar –r TimeInterval NoOfTimes
sar –r 60 60
safd -d /var/log/sa/sa20140903 -- -n DEV | grep -v lo

#check python paths: /usr/bin/python3 -> python3.7
ls -lh /usr/bin/python3


#In order to use xset & dpms commands, the screen blanking must be enabled in the GUI Raspberry pi config tool or sudo raspi-config
#Also xscreensaver must not be installed..
sudo apt remove -y xscreensaver
#sudo apt-get install -y python-gpiozero 
#sudo apt-get install -y python3-gpiozero
sudo apt install -y libgirepository1.0-dev

# https://kivy.readthedocs.io/en/master/installation/installation-rpi.html
sudo apt build-dep libsdl2
sudo apt-get install -y libsdl2-2.0 
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsdl2-2.0-0-dbgsym 

sudo adduser "$USER" render

sudo apt-get install -y lxhotkey-plugin-openbox
sudo apt-get install -y cubicsdr
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt full-upgrade

#https://askubuntu.com/questions/1025189/pip-is-not-working-importerror-no-module-named-pip-internal
#sudo apt-get install -y python3-dev python3-pil python3-pip 
#sudo apt-get install -y python3-pil.imagetk 
#or 
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
python get-pip.py --force-reinstall

#sudo pip config set global.no-cache-dir true
#sudo pip3 config set global.no-cache-dir true
#pip config set global.no-cache-dir true
#pip3 config set global.no-cache-dir true
#sudo reboot

#pip cache purge
#pip3 cache purge
#python -m pip cache purge
#python3 -m pip cache purge
#sudo python -m pip cache purge
#sudo python3 -m pip cache purge

sudo pip config set global.no-cache-dir false
sudo pip3 config set global.no-cache-dir false
pip config set global.no-cache-dir false
pip3 config set global.no-cache-dir false

python -m pip install --upgrade pip
sudo python -m pip install --upgrade pip
python3 -m pip install --upgrade pip
sudo python3 -m pip install --upgrade pip

python3 -m pip install --upgrade numpy pi3d svg.path rpi-gpio pygame
sudo python3 -m pip install --upgrade numpy pi3d svg.path rpi-gpio pygame


sudo su
if ! sudo grep -q max_usb_current "/boot/config.txt"; then
  echo "set setting"
  #echo 'max_usb_current=1' >> /boot/config.txt
  sudo cat <<EOF >> /boot/config.txt
max_usb_current=1
EOF
fi
if ! sudo grep -q safe_mode_gpio "/boot/config.txt"; then
  echo "set setting"
  #echo 'safe_mode_gpio=4' >> /boot/config.txt
  sudo cat <<EOF >> /boot/config.txt
safe_mode_gpio=4
EOF
fi

if ! sudo grep -q 'gpio-fan' "/boot/config.txt"; then
  echo "set setting"
  #echo 'dtoverlay=gpio-fan,gpiopin=14,temp=50000' >> /boot/config.txt
  sudo cat <<EOF >> /boot/config.txt
dtoverlay=gpio-fan,gpiopin=14,temp=50000
EOF
fi
if sudo grep -q 'gpio-fan' "/boot/config.txt"; then
  echo "set setting"
  #echo 'dtoverlay=gpio-fan,gpiopin=14,temp=50000' >> /boot/config.txt
  sudo sed -i 's/dtoverlay=gpio-fan,gpiopin=14,temp=50000/dtoverlay=gpio-fan,gpiopin=14,temp=55000/g' /boot/config.txt
fi


if ! sudo grep -q consoleblank "/boot/cmdline.txt"; then
  echo "set setting"
  sudo sed -i 's/rootwait/rootwait consoleblank=0 /g' /boot/cmdline.txt
fi
#sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt full-upgrade -y && sudo apt-get autoremove -y && sudo reboot
su pi

sudo su
if ! sudo grep -q watchdog "/boot/config.txt"; then
  echo "set setting"
  #echo 'dtparam=watchdog=on' >> /boot/config.txt
  sudo cat <<EOF >> /boot/config.txt
dtparam=watchdog=on
EOF
fi
if sudo grep -q '#max-load-1' "/etc/watchdog.conf"; then
  echo "set setting"
  sudo sed -i 's/#max-load-1/max-load-1/g' /etc/watchdog.conf
fi
if sudo grep -q '#min-memory' "/etc/watchdog.conf"; then
  echo "set setting"
  sudo sed -i 's/#min-memory/min-memory/g' /etc/watchdog.conf
fi
if sudo grep -q '#watchdog-device' "/etc/watchdog.conf"; then
  echo "set setting"
  sudo sed -i 's/#watchdog-device/watchdog-device/g' /etc/watchdog.conf
fi
if ! sudo grep -q watchdog-timeout "/etc/watchdog.conf"; then
  echo "set setting"
  #echo 'watchdog-timeout=15' >> /etc/watchdog.conf
  sudo cat <<EOF >> /etc/watchdog.conf
watchdog-timeout=15
EOF
fi
if sudo grep -q 'WantedBy=default.target' "/lib/systemd/system/watchdog.service"; then
  echo "set setting"
  sudo sed -i 's/WantedBy=default.target/WantedBy=multi-user.target/g' /lib/systemd/system/watchdog.service
fi
#maybe : echo 'interface = wlan0' >> /etc/watchdog.conf
sudo systemctl start watchdog
sudo systemctl enable watchdog
sudo systemctl daemon-reload
#test it with:     sudo bash -c ':(){ :|:& };:'
su pi

sudo su
if sudo grep -q London "/etc/timezone"; then
  echo "set setting"
  sudo sed -i 's+Europe/London+Europe/Berlin+g' /etc/timezone
fi

if sudo grep -q xserver-command "/etc/lightdm/lightdm.conf"; then
  echo "set setting"
  sudo sed -i '/xserver-command/s/^$/xserver-command=X -s 0 -p 0 -dpms/' /etc/lightdm/lightdm.conf
fi
su pi
#(When keyword is found, replace the entire line with newstuff)
#sed '/keyword/s/^$/newstuff/' filename
#For a really good SED tutorial, go here: http://www.grymoire.com/Unix/Sed.html
#https://stackoverflow.com/questions/525592/find-and-replace-inside-a-text-file-from-a-bash-command
#sed -i -e 's/rpi3/lisakaestner/g' /etc/samba/smb.conf
#var1=rpi3
#var2=lisakaestner
#sed -i -e 's/'"$var1"'/'"$var2"'/gi' /etc/samba/smb.conf
#sed -i 's/abc/XYZ/gi' /tmp/file.txt
#find ./ -type f -exec sed -i 's/rpi3/lisakaestner/gi' {} \;
#find ./ -iname "*.py" -type f -exec sed -i 's/abc/XYZ/gi' {} \;

#if ! grep -q stayOn "~/.bashrc"; then
#  echo "if [ $(tty) == /dev/tty1 ]; then
#  xinit /home/pi/aRadio/theRadio/stayOn.sh
#fi" > ~/.bashrc
#fi

# sudo nano /etc/xdg/lxsession/LXDE-pi/sshpwd.sh # and enter the following line as second line:
#return ${retVal} 2>/dev/null || exit ${retVal}

#      nano /home/pi/.config/lxsession/LXDE-pi/autostart # and enter the following lines below the cat command or:
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart # and enter the following lines below the cat command:
#https://stackoverflow.com/questions/11279335/bash-write-to-file-without-echo
sudo cat <<EOF > /etc/xdg/lxsession/LXDE-pi/autostart
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@xset s 0 0
@xset s noblank
@xset s noexpose
@xset dpms 0 0 0
#@unclutter -display :0 -idle 3 -root -noevents
@unclutter -idle 0.1
#@omxplayer -o hdmi "/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4"
#/home/pi/SDRplay/EASYplay.py
#/home/pi/aRadio/theRadio/janradio.py
#/home/pi/aRadio/theRadio/anneradio.py
#point-rpi
#@python3.6 /home/pi/aRadio/theRadio/jksnixieclock.py
#@python3 /home/pi/dcf77-reader-DF.py
#@python3 /home/pi/readClock.py -r 2000
#@python3 /home/pi/aRadio/theRadio/anneradio.py
@sh /home/pi/aRadio/theRadio/startit.sh
#@lxterminal --command "/home/pi/aRadio/theRadio/startit.sh"
#@lxterminal -e "/home/pi/aRadio/theRadio/startit.sh"
#@lxterminal -e "python3 /home/pi/readClock.py -r 2000"
#python3 /mnt/c/Users/theOperator/Dropbox/aRadio/theRadio/janradio.py
#export DISPLAY=:0 && python3 /mnt/c/Users/theOperator/Dropbox/aRadio/theRadio/janradio.py
@/home/pi/aRadio/theRadio/startit.sh
EOF

# Install the VS remote debugger on your Pi by running this command:
curl -sSL https://aka.ms/getvsdbgsh | /bin/sh /dev/stdin -v latest -l ~/vsdbg
# To debug you will need to run the program as root, so we'll need to be able to remote launch the program as root as well.


# https://www.linkedin.com/pulse/python-remote-debugging-visual-studio-code-raspberry-pi-mircea-dogaru


pip config set global.cache-dir false
pip config set global.no-cache-dir false
pip cache purge
rm -d -r "$(pip cache dir)"

sudo pkill -SIGKILL -f "python3" > /dev/null 2>&1
cd /home/pi
rm -fr "aRadio"
git config --global user.email "jan.kaestner@online.de" && git config --global user.name "Jan Kästner"
git clone "https://kaestnja:bc2de507d138f286dc7c9c94f9c41c41a7637b70@github.com/kaestnja/aRadio.git"
cd aRadio
git remote add origin git@github.com:kaestnja/aRadio.git
#git config --unset-all remote.origin.fetch
git fetch --all
git reset --hard origin/master
git pull -r
#rm -fr ".git/rebase-apply"

# exchange alle spaces in filenames for all files in a directory
#bash
find . -type f -exec sed -i -e 's/ /_/g' {} \;
#ps
cd C:\Users\janka\source\repos\github.com\kaestnja\aRadio\theRadio\fonts
Dir | Rename-Item –NewName { $_.name –replace “ “,”_” }
Get-ChildItem -Directory | Rename-Item –NewName { $_.name –replace “ “,”_” }

# export and import/install all installed apps
sudo dpkg-query -f '${binary:Package}\n' -W > packages_list_$HOSTNAME.txt
sudo xargs -a packages_list.txt apt install -y

git config --global user.email "jan.kaestner@online.de" && git config --global user.name "Jan Kästner"
cd /home/pi && rm -r /home/pi/aRadio
cd /home/pi && git clone "https://kaestnja:bc2de507d138f286dc7c9c94f9c41c41a7637b70@github.com/kaestnja/aRadio.git" &&  sudo chown -R pi /home && sudo chmod -R 6777 /home/pi/aRadio
#
cd /home/pi/aRadio && git config credential.helper store >/dev/null && git fetch "https://kaestnja:bc2de507d138f286dc7c9c94f9c41c41a7637b70@github.com/kaestnja/aRadio.git" && git stash && git pull && sudo chown -R pi /home && chmod -R 6777 /home/pi/aRadio
cd /home/pi/aRadio && git fetch --all >/dev/null && git reset --hard origin/master >/dev/null && git pull && sudo chown -R pi /home && chmod -R 6777 /home/pi/aRadio

cd /home/pi/aRadio/theRadio/fonts && sudo cp -r /home/pi/aRadio/theRadio/fonts/ /usr/local/share/


cd /home/pi && git clone "https://kaestnja:bc2de507d138f286dc7c9c94f9c41c41a7637b70@github.com/adafruit/Pi_Eyes.git" &&  sudo chown -R pi /home && sudo chmod -R 6777 /home/pi/Pi_Eyes


## to prepare to generate requirements.txt, if not already there:
# sudo pip3 install --upgrade pipreqs
# sudo sed -i 's/export PATH/PATH=$PATH:\/home\/pi\/.local\/bin\nexport PATH/g' /etc/profile
## generate requirements.txt, if not already there:
# cd /home/pi/aRadio/theRadio && pipreqs ./
## remove former wrong installed requirements
## sudo python3 -m pip uninstall -r /home/pi/aRadio/theRadio/requirements_old.txt -y
## sudo python3 -m pip uninstall fontconfig

# cd /home/pi/aRadio/theRadio && sudo python3 -m pip install -r /home/pi/aRadio/theRadio/requirements.txt
# cd /home/pi/aRadio/theRadio && pip3 install -r /home/pi/aRadio/theRadio/requirements.txt
# pip list --outdated
# pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U
# sudo pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 sudo pip3 install -U


#sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
#sudo su 
#passwd

#sudo sed -i 's+#/home/pi/SDRplay/EASYplay.py+/home/pi/SDRplay/EASYplay.py+g' /etc/xdg/lxsession/LXDE-pi/autostart
#sudo sed -i 's+/home/pi/aRadio/theRadio/janradio.py+#/home/pi/aRadio/theRadio/janradio.py+g' /etc/xdg/lxsession/LXDE-pi/autostart

sudo sed -i 's+/home/pi/SDRplay/EASYplay.py+#/home/pi/SDRplay/EASYplay.py+g' /etc/xdg/lxsession/LXDE-pi/autostart
sudo sed -i 's+#/home/pi/aRadio/theRadio/janradio.py+/home/pi/aRadio/theRadio/janradio.py+g' /etc/xdg/lxsession/LXDE-pi/autostart


#display
if [ -f /usr/share/dispsetup.sh ]; then
  echo "set setting"
  sudo rm /usr/share/dispsetup.sh
fi
# return ${retVal} 2>/dev/null || exit "${retVal}" to /home/pi/scripts/initDisplay.sh
if [ -f /home/pi/scripts/initDisplay.sh ]; then
  echo 1
  if ! grep -q retVal "/home/pi/scripts/initDisplay.sh"; then
    echo 2
    sed '2i Hello' /home/pi/scripts/initDisplay.sh > /home/pi/scripts/initDisplay_temp.sh
    sed -i 's+Hello+return ${retVal} 2>/dev/null || exit "${retVal}"+g' /home/pi/scripts/initDisplay_temp.sh
    rm /home/pi/scripts/initDisplay.sh
    mv /home/pi/scripts/initDisplay_temp.sh /home/pi/scripts/initDisplay.sh
    chmod +x /home/pi/scripts/initDisplay.sh
  fi
fi
if [ -f /etc/xdg/autostart/arandr-autostart.desktop ]; then
  echo "set setting"
  sudo rm /etc/xdg/autostart/arandr-autostart.desktop
fi
if [ -f /etc/xdg/autostart/pprompt.desktop ]; then
  echo "set setting"
  sudo rm /etc/xdg/autostart/pprompt.desktop
fi
# return ${retVal} 2>/dev/null || exit "${retVal}" to /home/pi/scripts/initDisplay.sh
if [ -f /etc/xdg/lxsession/LXDE-pi/sshpwd.sh ]; then
  echo 1
  if ! grep -q retVal "/etc/xdg/lxsession/LXDE-pi/sshpwd.sh"; then
    echo 2
    sudo sed '2i Hello' /etc/xdg/lxsession/LXDE-pi/sshpwd.sh > /etc/xdg/lxsession/LXDE-pi/sshpwd_temp.sh
    sudo sed -i 's+Hello+return ${retVal} 2>/dev/null || exit "${retVal}"+g' /etc/xdg/lxsession/LXDE-pi/sshpwd_temp.sh
    sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh
    sudo mv /etc/xdg/lxsession/LXDE-pi/sshpwd_temp.sh /etc/xdg/lxsession/LXDE-pi/sshpwd.sh
    sudo chmod +x /etc/xdg/lxsession/LXDE-pi/sshpwd.sh
  fi
fi




cd /home/pi/aRadio && for r in $(cat /home/pi/aRadio/theRadio/requirements.txt | grep -v ^#); do python3 -m pip install $r; done;

cd /home/pi/aRadio && for r in $(cat /home/pi/aRadio/theRadio/requirements.txt | grep -v ^#); do sudo python3 -m pip install $r; done;

cd /home/pi/aRadio && for r in $(cat /home/pi/aRadio/theRadio/requirements.txt | grep -v ^#); do python3 -m pip install --upgrade $r; done;

cd /home/pi/aRadio && for r in $(cat /home/pi/aRadio/theRadio/requirements.txt | grep -v ^#); do sudo python3 -m pip install --upgrade $r; done;

pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U
sudo pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 sudo pip3 install -U



# stream chromium
sudo apt-get install -y libwidevinecdm0 
sudo apt install --allow-unauthenticated
sudo apt-get install -y streamlink
#echo "deb http://deb.debian.org/debian buster-backports main" | sudo tee "/etc/apt/sources.list.d/streamlink.list"
#deb http://deb.debian.org/debian buster-backports main contrib non-free
sudo apt update
#sudo apt -t buster-backports install streamlink
# https://github.com/KenT2/tboplayer
cd ~ && wget https://github.com/KenT2/tboplayer/tarball/master -O - | tar xz && cd KenT2-tboplayer-* && chmod +x setup.sh && ./setup.sh
# or https://www.makeuseof.com/tag/raspberry-pi-chromecast/
tboplayer.cfg


# https://github.com/marcogrecopriolo/guglielmo
sudo apt-get install -y libsndfile-dev libsamplerate-dev libfaad-dev
cd /home/pi && rm -r /home/pi/guglielmo
cd /home/pi && git clone "https://kaestnja:bc2de507d138f286dc7c9c94f9c41c41a7637b70@github.com/marcogrecopriolo/guglielmo.git" &&  sudo chown -R pi /home && sudo chmod -R 6777 /home/pi/guglielmo
#
cd /home/pi/guglielmo && git config credential.helper store >/dev/null && git fetch "https://kaestnja:bc2de507d138f286dc7c9c94f9c41c41a7637b70@github.com/marcogrecopriolo/guglielmo.git" && git stash && git pull && sudo chown -R pi /home && chmod -R 6777 /home/pi/guglielmo
cd /home/pi/guglielmo && git fetch --all >/dev/null && git reset --hard origin/master >/dev/null && git pull && sudo chown -R pi /home && chmod -R 6777 /home/pi/guglielmo
cd ~ && cd guglielmo/
mkdir build
cd build
cmake ..
#or cmake .. -DRTLSDR=ON
make
sudo make install
sudo ldconfig


#if ! grep -q 2838 "/etc/udev/rules.d/20.rtlsdr.rules"; then
#  echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", GROUP="adm", MODE="0666", SYMLINK+="rtl_sdr"' > /etc/udev/rules.d/20.rtlsdr.rules
#fi
#cd /home/pi/aRadio/theRadio/rules.d && sudo cp -r /home/pi/aRadio/theRadio/rules.d/ /etc/udev/
sudo apt-get install -y libpulse-dev cmake g++ libpython-dev python-numpy swig libusb-1.0-0-dev libglib2.0-dev autotools-dev automake libgtk-3-dev libgtk-3-dev libgl-dev freeglut3-dev
sudo apt-get install -y libboost-dev libboost-filesystem-dev libboost-system-dev
cd ~
git clone git://git.osmocom.org/rtl-sdr.git
cd ~ && cd rtl-sdr/
mkdir build
cd build
#cmake ../
cmake ../ -DINSTALL_UDEV_RULES=ON
make
sudo make install
#sudo make install-udev-rules
sudo ldconfig

cd ~
git clone git://github.com/balint256/gr-baz.git
cd ~ && cd gr-baz
mkdir build
cd build
cmake ..
#cmake .. -DBoost_USE_STATIC_LIBS=ON
#OR
#cmake-gui ..
make
sudo make install
sudo ldconfig


cd ~
git clone https://github.com/pothosware/SoapySDR.git
cd ~ && cd SoapySDR
git pull origin master
mkdir build
cd build
cmake ..
make -j4
sudo make install
sudo ldconfig #needed on debian systems
SoapySDRUtil --info
#after new git pull
cd ~
cd SoapySDR
git pull origin master
cd build #use previous build directory, no need to run cmake again
make -j4
sudo make install
#repeat this step for projects that depend on SoapySDR
###########################################################################################

cd ~
git clone https://github.com/pothosware/SoapySDR.git
cd ~ && cd SoapySDR
mkdir build
cd ~ && cd SoapySDR && cd build
cmake ../ -DCMAKE_BUILD_TYPE=Release
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DLIB_INSTALL_DIR:PATH=lib64 -DLIB_SUFFIX=64 -DSOAPY_SDR_ROOT=/usr ..
make -j4
sudo make install
sudo ldconfig
SoapySDRUtil --info #test SoapySDR install


sudo apt-get install -y soapysdr-tools soapysdr-module-lms7 libsoapysdr-dev
sudo apt-get install -y git g++ cmake libsqlite3-dev
#install hardware support dependencies
sudo apt-get install -y libsoapysdr-dev libi2c-dev libusb-1.0-0-dev
#install graphics dependencies
sudo apt-get install -y libwxgtk3.0-dev freeglut3-dev
cd ~
git clone https://github.com/myriadrf/LimeSuite.git
cd LimeSuite
mkdir builddir && cd builddir
cmake ../
make -j4
sudo make install
sudo ldconfig
cd LimeSuite/udev-rules
sudo ./install.sh

cd ~
git clone https://github.com/pothosware/SoapySDR.git
cd ~ && cd SoapySDR
mkdir build
cd ~ && cd SoapySDR && cd build
cmake ../ -DCMAKE_BUILD_TYPE=Release
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DLIB_INSTALL_DIR:PATH=lib64 -DLIB_SUFFIX=64 -DSOAPY_SDR_ROOT=/usr ..
make -j4
sudo make install
sudo ldconfig
SoapySDRUtil --info #test SoapySDR install

SoapySDRUtil --probe="driver=sdrplay"

cd ~
git clone https://github.com/jgaeddert/liquid-dsp
cd ~ && cd liquid-dsp
./bootstrap.sh
CFLAGS="-march=native -O3" ./configure --enable-fftoverride 
make -j4
sudo make install
sudo ldconfig

cd ~
wget https://github.com/wxWidgets/wxWidgets/releases/download/v3.1.5/wxWidgets-3.1.5.tar.bz2
tar -xvjf wxWidgets-3.1.5.tar.bz2  
cd ~ && cd wxWidgets-3.1.5/
mkdir -p ~/Develop/wxWidgets-staticlib
./autogen.sh 
./configure --prefix=`echo ~/Develop/wxWidgets-staticlib` --with-opengl --disable-glcanvasegl --disable-shared --enable-monolithic --with-libjpeg --with-libtiff --with-libpng --with-zlib --disable-sdltest --enable-unicode --enable-display --enable-propgrid --disable-webview --disable-webviewwebkit CXXFLAGS="-std=c++0x"
#[ configuring.. ]
#make -j4 && make install
make -j4 && sudo make install
#[ building and installed to ~/Develop/wxWidgets-staticlib in this example ]
sudo ldconfig


sudo apt-get install -y gcc-5 g++-5 && sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/g++ g++ /usr/bin/g++-5 && sudo update-alternatives --set gcc "/usr/bin/gcc-5"
sudo apt-get install -y gcc-7 g++-7 && sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/g++ g++ /usr/bin/g++-7 && sudo update-alternatives --set gcc "/usr/bin/gcc-7"
cd ~
git clone https://github.com/cjcliffe/CubicSDR.git
cd ~ && cd CubicSDR
mkdir build
cd ~ && cd CubicSDR && cd build
#Add -DUSE_HAMLIB=1 to cmake command line to include hamlib support.
#For RasberryPi4, add -DOTHER_LIBS="-latomic"
#cmake ../ -DCMAKE_BUILD_TYPE=Release -DwxWidgets_CONFIG_EXECUTABLE=~/Develop/wxWidgets-staticlib/bin/wx-config -DOTHER_LIBS="-latomic"
cmake ../ -DOTHER_LIBRARIES:FILEPATH=/usr/lib/gcc/arm-linux-gnueabihf/8/libatomic.so -DCMAKE_BUILD_TYPE=Release -DwxWidgets_CONFIG_EXECUTABLE=~/Develop/wxWidgets-staticlib/bin/wx-config
#or
#adding the line SET(CMAKE_CXX_LINK_FLAGS "${CMAKE_CXX_LINK_FLAGS} -latomic") to the end of the CMakeLists.txt file in the CubicSDR
make && sudo make install
# You can now run the build from the folder, note if you're on 32-bit linux it will be in x86/
#cd x64/
#./CubicSDR
cd x86/
./CubicSDR


############################################################################################

#@xscreensaver -no-splash  # uncomment at /etc/xdg/lxsession/LXDE-pi/autostart
#@unclutter -display :0 -idle 3 -root -noevents # into /etc/xdg/lxsession/LXDE-pi/autostart

#PATH="${PATH}:/home/pi/aRadio/theRadio:/home/pi/grove.py:/usr/local/lib/python3.5:/usr/local/lib/python3.5/site-packages"
#export PATH
##:/home/pi/lib/python:/usr/local/lib/python2.7/site-packages
#PYTHONPATH="${PYTHONPATH}:/home/pi/aRadio/theRadio:/home/pi/grove.py:/usr/local/lib/python3.5:/usr/local/lib/python3.5/site-packages"
#export PYTHONPATH

# add at /home/pi/.bashrc :
#alias reboot='sudo pkill -f python* && sudo chmod -R 6777 /home && sudo chmod -R 6777 /root && sudo chown -R pi:pi /home/* && sudo reboot'
#alias update='sudo pkill -f python && pyclean . && sudo chmod -R 6777 /home && sudo chmod -R 6777 /root && sudo chown -R pi:pi /home/ && sudo apt --fix-broken install && sudo apt-get install --fix-missing && sudo apt-get update -y && sudo apt-get upgrade -y --force-yes && sudo apt-get clean -y --force-yes && sudo apt-get dist-upgrade -y --force-yes && sudo apt-get autoremove -y --force-yes && sudo apt-get autoclean -y --force-yes && sudo rpi-update && sudo reboot'
#alias swr1bw='omxplayer -o local http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
#alias dasding='omxplayer -o local http://swr-dasding-live.cast.addradio.de/swr/dasding/live/mp3/128/stream.mp3'
#alias swr3='omxplayer -o local http://swr-swr3-live.cast.addradio.de/swr/swr3/live/mp3/128/stream.mp3'
#alias rbb='omxplayer -o local http://rbb-fritz-live.cast.addradio.de/rbb/fritz/live/mp3/128/stream.mp3'
#alias mswr1bw='mplayer -quiet -cache 100 http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
#alias mdasding='mplayer -quiet -cache 100 http://swr-dasding-live.cast.addradio.de/swr/dasding/live/mp3/128/stream.mp3'
#alias mswr3='mplayer -quiet -cache 100 http://swr-swr3-live.cast.addradio.de/swr/swr3/live/mp3/128/stream.mp3'
#alias mrbb='mplayer -quiet -cache 100 http://rbb-fritz-live.cast.addradio.de/rbb/fritz/live/mp3/128/stream.mp3'
#xset s off > /dev/null 2>&1

# https://pi-buch.info/hdmi-ausgang-unkompliziert-ein-und-ausschalten/
# https://www.screenly.io/blog/2017/07/02/how-to-automatically-turn-off-and-on-your-monitor-from-your-raspberry-pi/
# https://pi-buch.info/hdmi-display-aus-und-wieder-einschalten/
# https://www.pcwelt.de/ratgeber/Linux-Autostart-Prozesse-entfernen-und-organisieren-9805724.html

#create menu entry via .desktop file
echo "[Desktop Entry]
Name=CubicSDR
GenericName=CubicSDR
Comment=Software Defined Radio
Exec=/opt/CubicSDR/CubicSDR
Icon=/opt/CubicSDR/CubicSDR.ico
Terminal=false
Type=Application
Categories=Network;HamRadio;" > /usr/share/applications/cubicsdr.desktop && sudo chown -R pi /home && chmod -R 6777 /home/pi/Desktop/cubicsdr.desktop

echo "[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=jan radio 
Exec=python3 /home/pi/aRadio/theRadio/janradio.py
#old
#Exec=gnome-terminal -e "bash -c '/home/pi/aRadio/theRadio/radioupdateshell.sh;$SHELL'"
Path=/home/pi/aRadio/theRadio
#Icon=/usr/share/pixmaps/python.xpm
Icon=/home/pi/aRadio/theRadio/bImages/earth-spinning-rotating-animation-24.gif
StartupNotify=true
Terminal=no
Hidden=false" > /usr/share/applications/janradio.desktop && sudo chown -R pi /home && chmod -R 6777 /home/pi/Desktop/janradio.desktop

echo "[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Name=jan radio new
Comment=Jan Radio
Exec=python3 /home/pi/aRadio/theRadio/janradio.py
#Exec=gnome-terminal -e "bash -c '/home/pi/aRadio/theRadio/radioupdateshell.sh;$SHELL'"
Path=/home/pi/aRadio/theRadio
Icon=/home/pi/aRadio/theRadio/bImages/earth-spinning-rotating-animation-24.gif
StartupNotify=true
Terminal=false
Hidden=false" > /home/pi/Desktop/janradionew.desktop && sudo chown -R pi /home && chmod -R 6777 /home/pi/Desktop/janradionew.desktop && chmod +x /home/pi/Desktop/janradionew.desktop

echo "[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Name=anne radio new
Comment=Anne Radio
Exec=python3 /home/pi/aRadio/theRadio/anneradio.py
#Exec=gnome-terminal -e "bash -c '/home/pi/aRadio/theRadio/radioupdateshell.sh;$SHELL'"
Path=/home/pi/aRadio/theRadio
Icon=/home/pi/aRadio/theRadio/bImages/earth-spinning-rotating-animation-24.gif
StartupNotify=true
Terminal=false
Hidden=false" > /home/pi/Desktop/anneradionew.desktop && sudo chown -R pi /home && chmod -R 6777 /home/pi/Desktop/anneradionew.desktop && chmod +x /home/pi/Desktop/anneradionew.desktop

#stream cast
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y libjpeg8-dev libpng12-dev
cd ~
git clone https://github.com/HaarigerHarald/omxiv
cd ~ && cd omxiv
make ilclient
make -j4
sudo make install

#dpkg -S /usr/lib/python2.7/dist-packages/FontTools
#dpkg -S /usr/lib/python2.7/dist-packages/fonttools
#dpkg -S /usr/local/lib/python3.5/dist-packages/FontTools
#dpkg -S /usr/local/lib/python3.5/dist-packages/fonttools
#nano ~/.themes/PiX/gtk-2.0/gtkrc
#gtk-enable-tooltips = 0
#/usr/share/icons/PiX

#return ${retVal} 2>/dev/null || exit ${retVal}
return ${retVal} 2>/dev/null || exit "${retVal}"

if [ 2 -lt 2 ]; then
    echo "set setting"
    sudo apt-get remove -y gcc-5-arm-linux-gnueabihf
    sudo apt-get remove --auto-remove gcc-5-arm-linux-gnueabihf
    sudo apt-get purge gcc-5-arm-linux-gnueabihf
    sudo apt-get purge --auto-remove gcc-5-arm-linux-gnueabihf
    sudo apt-get purge --auto-remove gcc-arm-linux-gnueabihf
    sudo pip uninstall -y FontTools
    sudo pip uninstall -y fonttools
    sudo pip3 uninstall -y FontTools
    sudo pip3 uninstall -y fonttools
    pip uninstall -y FontTools
    pip uninstall -y fonttools
    pip3 uninstall -y FontTools
    pip3 uninstall -y fonttools
    sudo apt remove -y FontTools
    sudo apt remove -y fonttools
    apt remove -y FontTools
    apt remove -y fonttools
    sudo apt-get autoremove -y --force-yes 
    sudo pip3 uninstall -y fontconfig
    sudo pip uninstall -y fontconfig
    sudo apt-get purge --auto-remove numpy scipy
    sudo apt remove -y numpy scipy
    sudo apt-get autoremove -y --force-yes 
    sudo apt-get purge --auto-remove python-numpy python-scipy
    sudo apt remove -y python-numpy python-scipy
    sudo apt-get autoremove -y --force-yes 
    sudo apt-get purge --auto-remove python3-numpy python3-scipy
    sudo apt remove -y python3-numpy python3-scipy
    sudo apt-get autoremove -y --force-yes 
    sudo pip3 uninstall -y numpy
    sudo pip uninstall -y numpy
    sudo apt-get autoremove -y --force-yes 
    sudo pip3 uninstall -y scipy
    sudo pip uninstall -y scipy
    sudo apt-get autoremove -y --force-yes 
    sudo apt remove -y banshee
    sudo apt remove -y banshee-extension-liveradio
    sudo apt remove -y banshee-extension-openvp
    sudo apt-get autoremove -y --force-yes 
    sudo apt-get remove -y chromium
    sudo apt-get purge -y chromium
    sudo apt-get purge -y chromium-browser
    rm .config/chromium -rf
    sudo apt install -f
    sudo apt-get autoremove -y --force-yes
    #fonttools ist schon die neueste Version (3.0-1).
    #sudo pip3 install fonttools
    #Requirement already satisfied: fonttools in /usr/local/lib/python3.5/dist-packages
    #sudo pip install fonttools
    #Requirement already satisfied: fonttools in /usr/lib/python2.7/dist-packages/FontTools
    #cp -r /mnt/c/____/DropBox/Dropbox/aRadio/theRadio/fonts/* /usr/local/share/fonts/
    #cp -r /mnt/d/__Dropbox/Dropbox/aRadio/theRadio/fonts/* /usr/local/share/fonts/
    #cp -r /root/Dropbox/aRadio/theRadio/fonts/* /usr/local/share/fonts/
    #####################################################
    sudo apt-get install -y fonttools
    sudo pip3 install --upgrade fonttools
    sudo pip3 install --proxy user:password@proxyserver:port pyxdameraulevenshtein
    sudo pip3 install --upgrade --proxy 141.73.108.181:8080 pyxdameraulevenshtein

    python3 /home/pi/aRadio/theRadio/anneradio.py
    python3 /mnt/c/Users/jk/OneDrive/py/0-vulnerabilities/main_qt.py
fi

if [ 2 -lt 2 ]; then
    echo "set setting"
    sudo pip3 install --upgrade pygame
    sudo python3 -mpip install pygame --upgrade
    sudo pip3 install --upgrade pip
    sudo pip3 install --upgrade pip setuptools
    sudo pip3 install --upgrade rpi.gpio
    sudo pip3 install --upgrade cffi
    sudo pip3 install --upgrade pycparser
    sudo pip3 install --upgrade dnspython
    sudo pip3 install --upgrade numpy
    sudo pip3 install --upgrade enum34
    sudo pip3 install --upgrade s-tui
    sudo pip3 install --upgrade psutil
    sudo pip3 install --upgrade pyaudio
    sudo pip3 install --upgrade pillow
    sudo pip3 install --upgrade pyalsaaudio
    sudo pip3 install --upgrade ipaddress
    sudo pip3 install --upgrade jedi
    sudo pip3 install --upgrade fontconfig
    sudo pip3 install --upgrade ply
    sudo pip3 install --upgrade Python-fontconfig
    sudo pip3 install --upgrade thonny
    sudo pip3 install --upgrade tkcolorpicker
    sudo pip3 install --upgrade pexpect
    sudo pip3 install --upgrade pysftp
    sudo pip3 install --upgrade tesserocr
    sudo pip3 install --upgrade pyocr
    sudo pip3 install --upgrade cryptography
    sudo pip3 install --upgrade paramiko
    
    #sudo pip3 install --upgrade wxPython
    #sudo pip3 install --upgrade wxPython-common
    #sudo pip3 install wxPython -v
    #sudo pip3 install --upgrade psutil
fi
if [ 2 -lt 2 ]; then
    echo "set setting"
    #pip3 freeze — local | grep -v ‘^\-e’ | cut -d = -f 1 | xargs -n1 pip3 install -U
    sudo pip3 freeze — local | grep -v ‘^\-e’ | cut -d = -f 1 | xargs -n1 sudo pip3 install -U
fi
if [ 2 -lt 2 ]; then
    echo "set setting"
    sudo apt-get update
    sudo apt-get install -y gcc-arm-linux-gnueabihf
    sudo apt-get install -y build-essential python3 python3-pip python3-dev python3-setuptools python3-numpy python3-tk python3-aiohttp python3-systemd idle3 python3-scipy
    sudo apt-get install -y python3-pil python3-pil.imagetk
    sudo apt-get install -y libatlas-base-dev libatlas-dev
    sudo apt-get install -y libsdl1.2-dev
    sudo apt-get install -y libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev 
    sudo apt-get install -y libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
    sudo apt-get install -y libfreetype6-dev
    sudo apt-get install -y subversion ffmpeg libavcodec-dev
    sudo apt-get install -y python3-pygame
    sudo apt-get install -y stress
    sudo apt-get install -y xscreensaver
    sudo apt-get install -y python3-matplotlib
    sudo apt-get install -y python3-pyaudio 
    sudo apt-get install -y python3-aubio
    #sudo apt-get install -y python3-thonny
    sudo apt-get install -y python3-fontconfig #import fontconfig; fontconfig.query()
    sudo apt-get install -y fontmatrix
    sudo apt-get install -y gnome-font-viewer
    sudo apt-get install -y font-manager
    sudo apt-get install -y libevent-dev
    sudo apt-get install -y hugin-tools
    sudo apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev
fi
if [ 2 -lt 2 ]; then
    echo "set setting"
    sudo apt-get install -y clearlooks-phenix-theme
    sudo apt-get install -y arc-theme
    sudo apt-get install -y gtk-theme-config
    sudo apt-get install -y gnome-tweak-tool
    sudo apt-get install -y agave
    sudo apt-get install -y gstreamer1.0-plugins-base
    sudo apt-get install -y gstreamer1.0-plugins-good
    sudo apt-get install -y gstreamer1.0-alsa
    sudo apt-get install -y gstreamer1.0-pulseaudio
    sudo apt-get install -y portaudio19-dev
    sudo apt-get install -y libasound2-dev
    sudo apt-get install -y alsa-utils
fi
#xscreensaver-demo

#for windows
#python -m pip install psutil
#python -m pip install pysftp
#python -m pip install python3-fontconfig
#python -m pip install Pillow
#python -m pip install pexpect
#
#####################################################


testseq="sky"
if [[ $the_hostname == *${testseq}* ]]; then
    echo "set setting"
    sudo pip list>"/root/pip_$the_hostname.txt"
    sudo pip3 list>"/root/pip3_$the_hostname.txt"
    sudo chown -R root:root root/Dropbox/aRadio && sudo chmod -R 6777 root/Dropbox/aRadio
    lsb_release -a && sudo apt-get install --fix-missing && sudo apt-get update -y
    sudo apt-get upgrade -y --force-yes && sudo apt-get clean -y --force-yes && sudo apt-get autoclean -y --force-yes && sudo apt-get autoremove -y --force-yes && sudo apt-get dist-upgrade -y && sudo apt-get update --fix-missing && sudo apt update && sudo apt install metasploit-framework && sudo msfupdate && sudo reboot
    exit 0
fi

testseq="kali"
if [[ $the_hostname == *${testseq}* ]]; then
    echo "set setting"
    sudo pip list>"/root/pip_$the_hostname.txt"
    sudo pip3 list>"/root/pip3_$the_hostname.txt"
    lsb_release -a && sudo apt-get install --fix-missing && sudo apt-get update -y
    sudo apt-get upgrade -y --force-yes && sudo apt-get clean -y --force-yes && sudo apt-get autoclean -y --force-yes && sudo apt-get autoremove -y --force-yes && sudo apt-get dist-upgrade -y && sudo apt-get update --fix-missing && sudo apt update && sudo apt install metasploit-framework && sudo msfupdate && sudo reboot
    exit 0
fi

testseq="rpi1"
if [[ $the_hostname == *${testseq}* ]]; then
    echo "set setting"
    sudo pip list>"/home/pi/aRadio/theRadio/pip_$the_hostname.txt"
    sudo pip3 list>"/home/pi/aRadio/theRadio/pip3_$the_hostname.txt"
    sudo chown -R pi:pi /home/pi/aRadio && sudo chmod -R 6777 /home/pi/aRadio
    sudo apt-get install --fix-missing && sudo apt-get update -y
    sudo apt-get upgrade -y --force-yes && sudo apt-get clean -y --force-yes && sudo apt-get dist-upgrade -y --force-yes && sudo apt-get autoremove -y --force-yes && sudo apt-get autoclean -y --force-yes && sudo rpi-update && cd /home/pi/LCD_show_v6_1_2/ && sudo /home/pi/LCD_show_v6_1_2/LCD35_v
    exit 0
fi

testseq="radio"
if [[ $the_hostname == *${testseq}* ]]; then
    echo "set setting"
    sudo pip list>"/home/pi/aRadio/theRadio/pip_$the_hostname.txt"
    sudo pip3 list>"/home/pi/aRadio/theRadio/pip3_$the_hostname.txt"
    sudo chown -R pi:pi /home/pi/aRadio && sudo chmod -R 6777 /home/pi/aRadio
    sudo apt-get install --fix-missing && sudo apt-get update -y
    sudo apt-get upgrade -y --force-yes && sudo apt-get clean -y --force-yes && sudo apt-get dist-upgrade -y --force-yes && sudo apt-get autoremove -y --force-yes && sudo apt-get autoclean -y --force-yes && sudo rpi-update && sudo reboot
    exit 0
fi


exit 1

##############################################################
#powershell
# Update the list of packages
sudo apt-get update
# Install pre-requisite packages.
sudo apt-get install -y wget apt-transport-https software-properties-common
# Download the Microsoft repository GPG keys
wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb
# Register the Microsoft repository GPG keys
sudo dpkg -i packages-microsoft-prod.deb
# Update the list of products
sudo apt-get update
# Install PowerShell
sudo apt-get install -y powershell
# Start PowerShell
pwsh
sudo apt-get install powershell

#or

sudo apt-get update
# install the requirements
sudo apt-get install -y \
        less \
        locales \
        ca-certificates \
        libicu63 \
        libssl1.1 \
        libc6 \
        libgcc1 \
        libgssapi-krb5-2 \
        liblttng-ust0 \
        libstdc++6 \
        zlib1g \
        curl

# Download the powershell '.tar.gz' archive
curl -L  https://github.com/PowerShell/PowerShell/releases/download/v7.1.3/powershell-7.1.3-linux-x64.tar.gz -o /tmp/powershell.tar.gz
# Create the target folder where powershell will be placed
sudo mkdir -p /opt/microsoft/powershell/7
# Expand powershell to the target folder
sudo tar zxf /tmp/powershell.tar.gz -C /opt/microsoft/powershell/7
# Set execute permissions
sudo chmod +x /opt/microsoft/powershell/7/pwsh
# Create the symbolic link that points to pwsh
sudo ln -s /opt/microsoft/powershell/7/pwsh /usr/bin/pwsh
# Start PowerShell
pwsh



########################################################################
#https://devdrik.de/upgrade-stretch-auf-buster/
#stretch to buster
cat /etc/os-release
sudo apt-get update && sudo apt-get upgrade -y
dpkg -C
apt-mark showhold

sudo sed -i 's/stretch/buster/g' /etc/apt/sources.list    
sudo sed -i 's/stretch/buster/g' /etc/apt/sources.list.d/raspi.list

grep -lnr stretch /etc/apt
sudo apt-get remove -y apt-listchanges

#sudo apt-get update && sudo apt-get upgrade -y
#sudo apt-get update && sudo apt-get full-upgrade -y
sudo apt-get update && sudo apt full-upgrade -y && sudo apt-get autoremove -y && sudo apt-get autoclean
sudo apt-get install -y apt-listchanges
cat /etc/os-release

sudo apt-get install debian-archive-keyring && sudo apt-key update


sudo rpi-update
#######################################################################
#https://www.circuitbasics.com/setup-lcd-touchscreen-raspberry-pi/
sudo nano /usr/share/X11/xorg.conf.d/99-fbturbo.conf
#Find the line that says Option "fbdev" "/dev/fb0" and change the fb0 to fb1:
#The fb0 option tells the video driver to output the display to HDMI, and the fb1 option tells it to output to the LCD screen
