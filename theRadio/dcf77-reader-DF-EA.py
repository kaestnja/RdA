#!/usr/bin/python3
r"""
    start auto as root:
crontab -e
    add line:
@reboot /home/pi/dcf77-reader-DF-EA.py &
    or start manual as pi:
sudo python3 ./dcf77-reader-DF-EA.py

    for windows:
pip install git+https://github.com/sn4k3/FakeRPi
pip3 install --upgrade git+https://github.com/sn4k3/FakeRPi

sudo apt-get install --fix-missing
sudo apt-get update -y
sudo apt-get upgrade -y --force-yes
sudo apt-get clean -y --force-yes
sudo apt-get dist-upgrade -y --force-yes
sudo apt-get autoremove -y --force-yes
sudo apt-get autoclean -y --force-yes
"""

import os
import time
import datetime

import RPi.GPIO as GPIO

# SIG (data from dcf) to SIG to Pin 10 GPIO 15 - the serial RxD, used by NTP
data_port = 15
data_pin = 10
# ENABLE (the dcf with low) to Pin 7 GPIO 4
enable_port = 4
enable_pin = 7
# LED (show the DCF IN as Led) to Pin 18 GPIO 24
led_port = 23
led_pin = 16

def clean_exit():
    GPIO.cleanup()
    exit()

def handler(signum, frame):
    clean_exit()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        # RPi.GPIO Layout verwenden (wie Pin-Nummern)
#GPIO.setmode(GPIO.BCM)            # RPi.GPIO Layout verwenden (wie GPIO-Nummern)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)

# Hautprogramm zum Abfragen des DCF77-Signals
GPIO.output(enable_pin, GPIO.LOW)
old_state = int(GPIO.input(data_pin))    # Zustand des DCFs einlesen
while True:
    GPIO.wait_for_edge(data_pin, GPIO.BOTH)
    old_state = int(GPIO.input(data_pin))
    # Angeschlossene LED an PIN led_pin blinken lassen um Sync. zu signalisieren
    if old_state == GPIO.HIGH:
        GPIO.output(led_pin, GPIO.HIGH)
    elif old_state == GPIO.LOW:
        GPIO.output(led_pin, GPIO.LOW)
