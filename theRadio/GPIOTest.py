from time import sleep
import RPi.GPIO as GPIO
from ky040.KY040 import KY040

CLOCKPIN1 = 23
DATAPIN1 = 24
SWITCHPIN1 = 18

CLOCKPIN2 = 4 #27
DATAPIN2 = 17
SWITCHPIN2 = 25 #22


def rotaryChange1(direction):
    print("turned 1 - " + str(direction))
def switchPressed1():
    print("button 1 pressed")
def rotaryChange2(direction):
    print("turned 2 - " + str(direction))
def switchPressed2():
    print("button 2 pressed")


GPIO.setmode(GPIO.BCM)

ky0401 = KY040(CLOCKPIN1, DATAPIN1, SWITCHPIN1, rotaryChange1, switchPressed1, rotaryBouncetime=50, switchBouncetime=500)
#ky0402 = KY040(CLOCKPIN2, DATAPIN2, rotaryCallback=rotaryChange2, rotaryBouncetime=50)
ky0402 = KY040(CLOCKPIN2, DATAPIN2, SWITCHPIN2, rotaryChange2, switchPressed2, rotaryBouncetime=50, switchBouncetime=500)

ky0401.start()
ky0402.start()

try:
    while True:
        #sleep(0.1)
        sleep(1)
finally:
    ky0401.stop()
    ky0402.stop()
    GPIO.cleanup()


    
