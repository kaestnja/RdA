#!/bin/bash
#https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/two.html
import RPi.GPIO as GPIO
import os
import subprocess
from time import sleep

path = "/var/omx_fifo"
if not os.path.exists(path):
    os.mkfifo(path)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def volumeUp(channel):
    print("Volume Up Pressed!")
    subprocess.call("volup", shell=True)
def volumeDown(channel):
    print("Volume Down Pressed!")
    subprocess.call("voldown", shell=True)
def audioStart(channel):
    print("Play Pressed")
    subprocess.call("audio-omx", shell=True)
    sleep(30)

GPIO.add_event_detect(23, GPIO.FALLING, callback=volumeUp, bouncetime=300)
GPIO.add_event_detect(24, GPIO.FALLING, callback=volumeDown, bouncetime=300)
GPIO.wait_for_edge(17, GPIO.FALLING)
subprocess.call("audio-omx", shell=True)

while True:
    GPIO.wait_for_edge(17, GPIO.FALLING)
    print("Play Pressed")
    os.system('audio-omx')
    os.system('omxstart')
    #subprocess.call("audio-omx", shell=True)
    #subprocess.call("omxstart", shell=True)
#sleep(30)

#amixer get Master
#amixer cset iface=MIXER,name="Master" [VALUE] >/dev/null

os.system('pkill omxplayer')
os.system("omxplayer -o local /home/pi/video/1.mp4")
os.system('sudo python example. py')

################################################################
#  This code allows me to playback the 30 secs audio whenever
#  I press the button so it loops ok, but doesn't do anything
#  apart from print "button 1" or "button 2" when they are pressed
#  so it doesn't affect the volume at all.  I got this code from another post on this forum I think and it helped get me closer!
################################################################

#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
import os
path = "/var/omx_fifo"
if not os.path.exists(path):
    os.mkfifo(path);

GPIO.setmode(GPIO.BCM)  
BUTTON_1 = 23
BUTTON_2 = 24
BUTTON_3 = 17
GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def Input_1(channel):
    print 'Button 1';
    os.system('voldown &');
def Input_2(channel):
    print 'Button 2';
    os.system('volup &');
def Input_3(channel):
    print 'Button 3';
    os.system('audio-omx &');
    sleep(30);

GPIO.add_event_detect(BUTTON_1, GPIO.BOTH, callback=Input_1, bouncetime=300) 
GPIO.add_event_detect(BUTTON_2, GPIO.BOTH, callback=Input_2, bouncetime=300)
GPIO.add_event_detect(BUTTON_3, GPIO.FALLING, callback=Input_3, bouncetime=300)
while True:
    sleep(60);


###################################################################
#  These are the shell scripts: audio-omx, volup, voldown, omxstart
###################################################################

###########
#  audio-omx
############

#!/bin/sh
sudo omxplayer -o local /home/pi/mediastore/test.mp3 & < /var/omx_fifo

###########
#  omxstart
###########

#!/bin/bash
echo -n '-' > /var/omx_fifo

##########
#  volup
##########

#!/bin/sh
echo -n '+' > /var/omx_fifo

##########
# voldown
##########

#!/bin/sh
echo -n '-' > /var/omx_fifo
