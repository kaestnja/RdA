#!/usr/bin/env python3
################################################################
# sudo apt-get install python-rpi.gpio 
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
################################################################
# https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/turing-machine/two.html
# https://github.com/popcornmix/omxplayer
# https://www.python-kurs.eu/tkinter_labels.php
# http://effbot.org/zone/tkinter-scrollbar-patterns.htm
# https://www.python-kurs.eu/tkinter_labels.php

import RPi.GPIO as GPIO
import os
import sys
import subprocess
import tkinter
from tkinter import ttk
from time import sleep
from subprocess import Popen
from omxplayer.player import OMXPlayer
from pathlib import Path

print ("start")
os.system('pkill omxplayer')
os.system('killall omxplayer.bin') 
path = "/var/omx_fifo"
if not os.path.exists(path):
    os.mkfifo(path);

# Set the mode of numbering the pins. 
# GPIO.setmode(GPIO.BOARD) 
GPIO.setmode(GPIO.BCM)
pin = 1
if pin:
    BUTTON_CU = 4
    BUTTON_CD = 17
    BUTTON_VU = 18
    BUTTON_VD = 22
    RELAIS_ON = 23
    RELAIS_OFF = 24
else:
    BUTTON_CU = 7
    BUTTON_CD = 11
    BUTTON_VU = 12
    BUTTON_VD = 15
    RELAIS_ON = 16
    RELAIS_OFF = 18

#GPIO.setup(BUTTON_VU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(BUTTON_VD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_CU, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
#GPIO.setup(BUTTON_CD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(RELAIS_ON, GPIO.OUT)
#GPIO.setup(RELAIS_OFF, GPIO.OUT)

#mswr1bw='mplayer -quiet -cache 100 http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
#swr1bw='omxplayer -o local http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
#omxplayer --win '100 100 500 500'
swr1bw='http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
dasding='http://swr-dasding-live.cast.addradio.de/swr/dasding/live/mp3/128/stream.mp3'
swr3='http://swr-swr3-live.cast.addradio.de/swr/swr3/live/mp3/128/stream.mp3'
rbb='http://rbb-fritz-live.cast.addradio.de/rbb/fritz/live/mp3/128/stream.mp3'

#https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

def volumeUp():
    print("Button volumeUp")
    #subprocess.call("volup", shell=True)
def volumeDown():
    print("Button volumeDown")
    #subprocess.call("voldown", shell=True)
def channelUp():
    print("Button channelUp")
    #subprocess.call("chup", shell=True)
    #os.system('pkill omxplayer')
    #omxc = Popen(['omxplayer', '-o','local', swr1bw])
    #mc = Popen(['mplayer', '-quiet','-cache','100', swr1bw])
    #subprocess.call(["dbuscontrol.sh","setvideopos", x1 , y2 , x2 , y1])
    player = OMXPlayer(swr1bw)
    sleep(8)
    player.quit()
def channelDown():
    print("Button channelDown")
    #subprocess.call("chdown", shell=True)
    videoPlayer = '/usr/bin/lxterminal -e /usr/bin/omxplayer '
    command = videoPlayer + '\x22' + videoFile + '\x22'
    subprocess.call(command, shell=True)

#GPIO.add_event_detect(BUTTON_VU, GPIO.FALLING, callback=volumeUp, bouncetime=300) 
#GPIO.add_event_detect(BUTTON_VD, GPIO.FALLING, callback=volumeDown, bouncetime=300)
GPIO.add_event_detect(BUTTON_CU, GPIO.RISING, callback=channelUp, bouncetime=300)
#GPIO.add_event_detect(BUTTON_CD, GPIO.FALLING, callback=channelDown, bouncetime=300)

# Initialise GPIO10 to high (true) so that the LED is off.
#GPIO.output(16, True) 
#while 1: 
#    if GPIO.input(7): 
#        GPIO.output( 16, False) 
#    else: 
#        # When the button switch is not pressed, turn off the LED. 
#        GPIO.output( 16, True)

#top = tkinter.Tk()
#canvas = tkinter.Canvas(top)
#canvas.grid(row = 0, column = 0)
#photo = tkinter.PhotoImage(file = './blah.jpg')
#canvas.create_image(0,0, image=photo)
#top.mainloop()


#fenster = tkinter.Tk()
#def hauptteil():
#    rahmen = tkinter.Frame()
#    rahmen.pack()
#    text = tkinter.Label(rahmen, text='Siehe da, ein Fenster!')
#    text.pack()

#hauptteil()
#fenster.mainloop()


while True:
    print("loop")
    sleep(3)

#amixer get Master
#amixer cset iface=MIXER,name="Master" [VALUE] >/dev/null

#os.system('pkill omxplayer')
#os.system("omxplayer -o local /home/pi/video/1.mp4")
#os.system('sudo python omx-tini-1.py')
