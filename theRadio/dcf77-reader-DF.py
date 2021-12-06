#!/usr/bin/python3
r"""
    start auto as root:
crontab -e
    add line:
@reboot /home/pi/dcf77-reader-DF.py &
    or start manual as pi:
sudo python3 ./dcf77-reader-DF.py
sudo python3 /home/pi/aRadio/theRadio/dcf77-reader-DF.py
sudo python3 /home/pi/aRadio/theRadio/aClock/Clock.py
git clone "https://kaestnja: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@github.com/kaestnja/aRadio.git"
cd /home/pi/aRadio && git pull && sudo python3 /home/pi/aRadio/theRadio/dcf77-reader-DF.py

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
pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U
Die Sekundenmarken mit einer Dauer von 0,1 s entsprechen der binären Null, die mit einer Dauer von 0,2 s der binären Eins. Die 59 Sekunde bleibt aus, die 0 Sekunde ist immer ein LOW.
https://www.dcf77logs.de/live

https://www.meteotime.com/regionen/
Forecast center Stuttgart Region ID 59
Forecast center Frankfurt Region ID 12
Forecast center Donaueschingen Region ID 57
Forecast center Strassburg Region ID 45
http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-DCF77/
http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-RTC/index.html
https://www.pipperr.de/dokuwiki/doku.php?id=raspberry:dcf77_modul
http://www.ptb.de/cms/de/fachabteilungen/abt4/fb-44/ag-442/dissemination-of-legal-time/dcf77.html
http://www.ptb.de/cms/fachabteilungen/abt4/fb-44/ag-442/verbreitung-der-gesetzlichen-zeit/dcf77/zeitcode.html
"""
import importlib.util
import os
import time
import datetime
#from datetime import datetime
#from datetime import timedelta
#from datetime import timestamp
from array import *

try:
    # Check and import real RPi.GPIO library
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
    # or
    # importlib.util.find_spec('RPIO')
    # import RPIO as GPIO
except ImportError:
    # If real RPi.GPIO library fails, load one of the fake one
    # import FakeRPi.RPiO as RPiO
    # or
    import FakeRPi.GPIO as GPIO

# running endless if true
Scanning = True
# for debug prints
PrintVerbose = True
# globals for valdidation in sub "decodeDCF77"
yearold = 9999
monthold = 99
dayold = 99
hourold = 99
# inits for main loop
begin_found = False
begin_bit_found = False
bit_seq = [int] * 59
first_round = True
counterDCFsig = 0
counterDCFsigold = 0
counterForLog = 0

os.system("sudo service ntp stop")
# SIG (data from dcf) to SIG to Pin 10 GPIO 15 - the serial RxD, used by NTP
data_port = 15
data_pin = 10
# ENABLE (the dcf with low) to Pin 7 GPIO 4
enable_port = 4
enable_pin = 7
# LED (show the DCF IN as Led) to Pin 18 GPIO 24
led_port = 23
led_pin = 16

# ######  define the handler if the program is stopped with ^c ######
# Clean exit!
def clean_exit():
    GPIO.cleanup()
    os.system("sudo service ntp start")
    exit()

# define the handler if the program is stopped with ^c
def handler(signum, frame):
    print ("Catch Error " + str(signum) + " - frame :: " + str(frame) + "")
    clean_exit()

# Unterprogramm zum Umwandeln BCD nach Dezimal
def bcd2dez(b3, b2, b1, b0):
    result = b0 + b1 * 2 + b2 * 4 + b3 * 8
    return result

# Paritaetspruefung (gerade P.)
# Es werden der Start- und Ende-Index im Array angegeben
def parity(start, end, bit_arr):
    i = start
    ipar = 0
    while i <= end:
        ipar = ipar + bit_arr[i]
        i = i + 1
    return (ipar % 2)

# Unterprogramm zum Decodieren des DCF77-Signals
def decodeDCF77(bit_seq,thePrintVerbose):
    global yearold
    global monthold
    global dayold
    global hourold

    if bit_seq[0] != 0 or bit_seq[20] != 1:
        return None
    # Minute (BCD) berechnen
    minute = bcd2dez(bit_seq[24], bit_seq[23], bit_seq[22], bit_seq[21])
    minute = minute + 10 * bcd2dez(0, bit_seq[27], bit_seq[26], bit_seq[25])
    if parity(21, 27, bit_seq) != bit_seq[28]:
        return None
    # Stunde (BCD) berechnen
    hour = bcd2dez(bit_seq[32], bit_seq[31], bit_seq[30], bit_seq[29])
    hour = hour + 10 * bcd2dez(0, 0, bit_seq[34], bit_seq[33])
    if parity(29, 34, bit_seq) != bit_seq[35]:
        return None
    # Jahr (BCD) berechnen
    year = bcd2dez(bit_seq[53], bit_seq[52], bit_seq[51], bit_seq[50])
    year = year + 10 * bcd2dez(bit_seq[57], bit_seq[56], bit_seq[55], bit_seq[54]) + 2000
    # Monat (BCD) berechen
    month = bcd2dez(bit_seq[48], bit_seq[47], bit_seq[46], bit_seq[45]) + bit_seq[49] * 10
    # Tag (BCD) berechnen
    day = bcd2dez(bit_seq[39], bit_seq[38], bit_seq[37], bit_seq[36])
    day = day + 10 * bcd2dez(0, 0, bit_seq[41], bit_seq[40])
    if parity(36, 57, bit_seq) != bit_seq[58]:
        return None
    if minute >= 60 or hour >= 24 or day <= 0 or day >= 32 or month <= 0 or month >= 13 or year >= 2030 or year <= 2018:
        return None

    if thePrintVerbose:
        print ("\nDie erkannte Zeit:                   " + str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute))
    # Pruefen des Datums aus vorangegangenem Lauf
    if year != yearold or month != monthold or day != dayold or hour != hourold:
        if thePrintVerbose:
            print ("ist ungleich der alten Referenzzeit: " + str(yearold) + "-" + str(monthold) + "-" + str(dayold) + " " + str(hourold) + ":XX")
        yearold = year
        monthold = month
        dayold = day
        hourold = hour
        if thePrintVerbose:
            print ("Setze Referenzzeit und wiederhole DCF77 Auswertung")
        return None
    if thePrintVerbose:
        print ("Ist gleich der alten Referenzzeit:   " + str(yearold) + "-" + str(monthold) + "-" + str(dayold) + " " + str(hourold) + ":XX")

    # Umrechnen ins datetime-Format
    second = 0
    microsecond = 0
    dcf77_time = datetime.datetime(year, month, day, hour, minute, second, microsecond)
    return dcf77_time

def percentof(percent, whole):
  return (percent * whole) / 100.0

# test for 1s lasts: 0:00:01.001443
# test for 0.001s lasts: 0:00:00.001395
# fuer neuere Raspberries (z. B. Pi 2 mit 4 Kernen):
# wenn die Dekodierung nicht klappt statt 110000 besser 140000 verwenden
decoderconstant = 140000

start_time = datetime.datetime.now()
time.sleep(1)
one_sec_time_low = datetime.datetime.now() - start_time
print ("test for 1s lasts:     " + str(one_sec_time_low))
start_time = datetime.datetime.now()
time.sleep(0.001)
one_msec_time_low = datetime.datetime.now() - start_time
print ("test for 0.001s lasts: " + str(one_msec_time_low))
start_time = datetime.datetime.now()
time.sleep(1.5)
dt = datetime.datetime.now() - start_time
start_time = datetime.datetime.now()
time.sleep(1.9)
one_sec_time_high = datetime.datetime.now() - start_time
if (one_msec_time_low < one_sec_time_low < dt < one_sec_time_high):
    print ("test one_sec_time_low : " + str(one_sec_time_low))
    print ("test dt               : " + str(dt))
    print ("test one_sec_time_high: " + str(one_sec_time_high))
    print ("simple time test: ok")

# supress warning
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        # RPi.GPIO Layout verwenden (wie Pin-Nummern)
#GPIO.setmode(GPIO.BCM)            # RPi.GPIO Layout verwenden (wie GPIO-Nummern)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)

# Hautprogramm zum Abfragen des DCF77-Signals
GPIO.output(enable_pin, GPIO.LOW)
old_state = int(GPIO.input(data_pin))    # Zustand des DCFs einlesen
#os.system("echo " + str(start_time) + " decoderconstant=" + str(decoderconstant) + " > /home/pi/dcf77-reader-DF-log.txt")

# Schleife, bis das Signal decodiert wurde
if PrintVerbose:
    print ("----------Referenzdatum gesetzt auf: " + str(hourold) + ":XX:XX am " + str(dayold) + "." + str(monthold) + "." + str(yearold))
while Scanning:
    counterDCFsigold = counterDCFsig
    # Get microseconds dt.microsecond
    if first_round:
        start_time = datetime.datetime.now()
        first_round = False
        if PrintVerbose:
            print ("1...Warte auf Minutenbeginn .............................60")
    GPIO.wait_for_edge(data_pin, GPIO.BOTH)
    # Zeit vom letzten Pegelwechsel am Eingang
    dt = datetime.datetime.now() - start_time
    start_time = datetime.datetime.now()

    #if dt.seconds == 1:    # Minutenbeginn bei Zeitdauer ca 1,7 s, Null any
    if one_sec_time_low < dt < one_sec_time_high:
        begin_bit_found = True
        begin_found = False
        bit_seq = [int] * 59
        if PrintVerbose: 
            print("0", end='')
        counterDCFsig = 0
        counterDCFsigold = 0
    elif old_state == GPIO.HIGH and begin_bit_found and dt.microseconds < decoderconstant:
        begin_bit_found = False
        begin_found = True
        counterDCFsig = 0
        bit_seq[counterDCFsig] = 0
        #if PrintVerbose: print(str(0), end='')
        if PrintVerbose:
            print("X", end='')
        #print (str(time.time()) + "   " + str(counterDCFsig) + " " + str(0))
    elif begin_found and old_state == GPIO.HIGH:
        counterDCFsig = counterDCFsig + 1
        bit_seq[counterDCFsig] = 0 if int(dt.microseconds) < decoderconstant else 1
        if PrintVerbose: 
            print (str(bit_seq[counterDCFsig]), end='')
            #print (str(time.time()) + "   " + str(counterDCFsig) + " " + str(bit_seq[counterDCFsig])) 
        # vorletzte Sekunde
        if counterDCFsig == 58:
            #0010011000001100100100011011110010111101001010010100110000
            #0011111110100100110011010110010111101001010010100110000
            #0101110101001000100100000000001010011101001010010100110000
            #0101101011000100100110000001001010011101001010010100110000
            #00101100010000100100111100001101010111101001010010100110000
            #0-10111001001001-001001-11001100-0010100-000001-101-10010-100110000
            begin_found = False
            bit_str = ''.join(str(bit) for bit in bit_seq)
            #bit_str = ''.join(bit_seq)
            dcf77_time = decodeDCF77(bit_seq, True)
            if dcf77_time is not None:
                time_date_str = "\"{:4d}-{:02d}-{:02d} {:02d}:{:02d}:00\"".format(dcf77_time.year, dcf77_time.month, dcf77_time.day, dcf77_time.hour, dcf77_time.minute)
                # letzte Sekunde abwarten
                if decoderconstant == 140000:
                    time.sleep(1.845)
                else:
                    time.sleep(1)
                # Date/Time-String formatieren
                datetime_now = datetime.datetime.now()
                dcf77_time_jitter = datetime.datetime.now() - dcf77_time
                datetime_now_str = "\"{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}\"".format(datetime_now.year, datetime_now.month, datetime_now.day, datetime_now.hour, datetime_now.minute, datetime_now.second)
                if not (time_date_str in datetime_now_str):
                    # Systemzeit setzen
                    #os.system("date -s " + time_date_str + " > /dev/null")
                    #os.system("echo " + " at Pi time:" + str(datetime.datetime.now()) + " DCF time was: " + time_date_str + " jitter: " + str(dcf77_time_jitter) + " >> /home/pi/dcf77-reader-DF-corrected.txt")
                    if PrintVerbose:
                        #print ("\nSystemzeit setzen via " + "   " + "date -s " + str(time_date_str) + " > /dev/null")
                        print (" at Pi time:" + str(datetime.datetime.now()) + " DCF time was: " + str(dcf77_time))
                else:
                    counterForLog = counterForLog + 1
                    if (counterForLog >= 100):
                        counterForLog = 0
                        #os.system("echo " + " at Pi time:" + str(datetime.datetime.now()) + " DCF time was: " + time_date_str + " jitter: " + str(dcf77_time_jitter) + " > /home/pi/dcf77-reader-DF-proofed.txt")
                    #else:
                        #os.system("echo " + " at Pi time:" + str(datetime.datetime.now()) + " DCF time was: " + time_date_str + " jitter: " + str(dcf77_time_jitter) + " >> /home/pi/dcf77-reader-DF-proofed.txt")
                #os.system("echo " + " at Pi time:" + str(datetime.datetime.now()) + " DCF time was: " + time_date_str + " >> /home/pi/dcf77decode.txt")
            if PrintVerbose: 
                print(bit_str)
                print (" at Pi time:" + str(datetime.datetime.now()) + " DCF time was: " + str(dcf77_time))
                #os.system("echo " + " at Pi time:" + str(datetime.datetime.now()) + " DCF was: " + bit_str + " >> /home/pi/dcf77.txt")
                #Scanning = False

    old_state = int(GPIO.input(data_pin))
    # Angeschlossene LED an PIN led_pin blinken lassen um Sync. zu signalisieren
    if old_state == GPIO.HIGH:
        GPIO.output(led_pin, GPIO.HIGH)
    elif old_state == GPIO.LOW:
        GPIO.output(led_pin, GPIO.LOW)
