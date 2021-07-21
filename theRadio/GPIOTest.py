from time import sleep
import RPi.GPIO as GPIO
from ky040.KY040 import KY040
import socket

# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

the_hostname = socket.gethostname()

CLOCKPINVOLUMN = 23
DATAPINVOLUMN = 24
SWITCHPINVOLUMN = 18

CLOCKPINSTATION = 27
DATAPINSTATION = 17
SWITCHPINSTATION = 22

if ('pi4radio1' in the_hostname or 'pi4radio2' in the_hostname):
    CLOCKPINSTATION = 4 #27
    DATAPINSTATION = 17
    SWITCHPINSTATION = 25 #22

def rotaryChangeVolumn(direction):
    print("turned Volumn - " + str(direction))
def switchPressedVolumn():
    print("button Volumn pressed")
def rotaryChangeStation(direction):
    print("turned Station - " + str(direction))
def switchPressedStation():
    print("button Station pressed")

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

ky040Volumn = KY040(CLOCKPINVOLUMN, DATAPINVOLUMN, SWITCHPINVOLUMN, rotaryChangeVolumn, switchPressedVolumn, rotaryBouncetime=50, switchBouncetime=500)
#ky040Station = KY040(CLOCKPINSTATION, DATAPINSTATION, rotaryCallback=rotaryChangeStation, rotaryBouncetime=50)
ky040Station = KY040(CLOCKPINSTATION, DATAPINSTATION, SWITCHPINSTATION, rotaryChangeStation, switchPressedStation, rotaryBouncetime=50, switchBouncetime=500)

ky040Volumn.start()
ky040Station.start()

try:
    while True:
        #sleep(0.1)
        sleep(1)
finally:
    ky040Volumn.stop()
    ky040Station.stop()
    GPIO.cleanup()


    
