from time import sleep
import RPi.GPIO as GPIO
from ky040.KY040 import KY040

CLOCKPIN1 = 23
DATAPIN1 = 24
SWITCHPIN1 = 18

CLOCKPIN2 = 27
DATAPIN2 = 17
SWITCHPIN2 = 22


def rotaryChange1(direction):
    print("turned - " + str(direction))
def switchPressed1():
    print("button pressed")
def rotaryChange2(direction):
    print("turned - " + str(direction))
def switchPressed2():
    print("button pressed")


GPIO.setmode(GPIO.BCM)

ky0401 = KY040(CLOCKPIN1, DATAPIN1, SWITCHPIN1, rotaryChange1, switchPressed1)
ky0402 = KY040(CLOCKPIN2, DATAPIN2, SWITCHPIN2, rotaryChange2, switchPressed2)

ky0401.start()
ky0402.start()

try:
    while True:
        sleep(0.1)
finally:
    ky0401.stop()
    ky0402.stop()
    GPIO.cleanup()


    
