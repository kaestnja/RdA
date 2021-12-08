#!/bin/bash
# coding=utf-8

# git config --global core.autocrlf input
# cd /home/pi/aRadio && git config credential.helper store >/dev/null && git fetch "https://kaestnja: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@github.com/kaestnja/aRadio.git" && git stash && git pull && sudo chown -R pi /home && chmod -R 6777 /home/pi/aRadio
# cd /home/pi/aRadio && git config credential.helper store && git fetch --all >/dev/null && git reset --hard origin/master >/dev/null && git pull && sudo chown -R pi /home && chmod -R 6777 /home/pi/aRadio

DISPLAY=:0.0; export DISPLAY;

if [[ $(hostname) = "pi4radio1" ]] || [[ $(hostname) == "rpi3" ]]; then
    echo "either pi4radio1 or rpi3 identified";
    #sudo pkill -f python*;
    #sudo pkill -f python;
    #sudo pkill -f omxplayer;
    #sudo pkill -f chromium;
    sudo pkill -SIGKILL -f "python3" > /dev/null 2>&1;
    sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1;
    sudo pkill -SIGKILL -f "omxplayer.bin" > /dev/null 2>&1;
    sudo pkill -SIGKILL -f "chromium" > /dev/null 2>&1;

    #sudo killall -9 omxplayer;
    #sudo killall -9 "omxplayer.bin";
else
    echo "neither pi4radio1 nor rpi3 identified";
fi

if [[ $(hostname) = "pi4radio1" ]] || [[ $(hostname) == "pi4radio2" ]] || [[ $(hostname) == "pi4radio3" ]]; then
    echo "pi4radio1 identified";
    sudo dhclient -v;
    omxplayer -o alsa:hw:0,0 "/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4";
    #python3 /home/pi/aRadio/theRadio/anneradio.py;
    python3 /home/pi/aRadio/theRadio/janradio.py;
    #python3 /home/pi/aRadio/theRadio/KY040/examples/python3.py;
fi
if [[ $(hostname) = "pi3radio2" ]]; then
    echo "pi4radio1 identified";
    sudo dhclient -v;
    omxplayer -o hdmi "/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4";
    #python3 /home/pi/aRadio/theRadio/anneradio.py;
    python3 /home/pi/aRadio/theRadio/janradio.py;
    #python3 /home/pi/aRadio/theRadio/KY040/examples/python3.py;
fi
if [[ $(hostname) = "rpi3" ]]; then
    echo "rpi3 identified";
    sleep 15;
    omxplayer -o local "/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4";
    python3 /home/pi/aRadio/theRadio/anneradio.py;
fi
exit 0

case $HOSTNAME in
    #(pi4radio1) omxplayer -o hdmi "/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4";;
    #(rpi3) omxplayer -o local "/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4";;
    (*)   echo "How did I get in the middle of nowhere?";;
esac

case $HOSTNAME in
    #(pi4radio1) /home/pi/aRadio/theRadio/janradio.py;;
    #(rpi3) /home/pi/aRadio/theRadio/anneradio.py;;
    (*)   echo "How did I get in the middle of nowhere?";;
esac


#omxplayer -o hdmi "/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4"
#/home/pi/aRadio/theRadio/janradio.py
#/home/pi/aRadio/theRadio/anneradio.py
#python3 /home/pi/aRadio/theRadio/anneradio.py > /dev/null 2>&1

# DISPLAY=:0 python3 /home/pi/aRadio/theRadio/anneradio.py &
# DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/anneradio.py
#/home/pi/aRadio/theRadio/startit_switch.sh &
#/home/pi/aRadio/theRadio/startit_switch.sh > /dev/null 2>&1

#omxplayer --blank /home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4 &
#omxplayer -o local '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4' --win '0 0 800 480'
#DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4'
#exec xterm -fn fixed -fullscreen -fg black -bg black -e omxplayer -o hdmi --no-osd --loop -r "$1""
exit 0 

#http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_GPIO_Shell.html
