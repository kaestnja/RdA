#!/bin/bash
#*/1 * * * * /home/pi/aRadio/theRadio/check_connection.sh

#40 3 * * * ps axeuf >> /root/reboot.log 2>&1
#30 3 * * * reboot >> /root/reboot.log 2>&1
#44 3 * * * /bin/date >> /root/reboot.log 2>&1
#45 3 * * * /sbin/shutdown -r now >> /root/reboot.log 2>&1
#@reboot /bin/echo "reboot check it via: sudo crontab -e" >> /root/reboot.log 2>&1
#@reboot /bin/date >> /root/reboot.log 2>&1
@reboot /bin/echo "reboot check it via: sudo crontab -e" >> /home/pi/reboot.log 2>&1
@reboot /bin/date >> /home/pi/reboot.log 2>&1

DST=192.168.178.1
if ! ping -c 5 -t 5 $DST > /dev/null
then
  #/usr/bin/logger "Restarting wlan0 network driver"
  #/usr/sbin/rmmod brcmfmac && /usr/sbin/modprobe brcmfmac roamoff=1
  reboot
fi

while :
do
  if ping -c 1 $DST &> /dev/null
  then
    echo "Host is online"
    break
  fi
  sleep 5
done
