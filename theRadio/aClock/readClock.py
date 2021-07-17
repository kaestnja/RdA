__author__ = 'gpipperr'

"""
Small Python Script to decode a DFC77 Module connect to the Raspberry 

# SIG (data from dcf) to SIG to Pin 11 GPIO 17
data_port = 17
data_pin = 11
# ENABLE (the dcf with low) to Pin 7 GPIO 4
enable_port = 4
enable_pin = 7
# LED (show the DCF in as Led) to Pin 18 GPIO 24
led_port = 24
led_pin = 18

Parameter -d  To supress the debug output start the script with -d 01
Parameter -r  Define how often the time will be read
Paramter -e  Not anlyse in the middle of the datagramm between 300ms and 900ms to save CPU
Parameter -s  set the OS Clock to the last captured time

Example:  run 30 minutes and show no Debug Messages and not use the energy mode to save CPU and not set the OS clock
python readClock.py -r 30 -d  0 -e 0 -s 0
"""

import os
import time
import RPIO

import datetime
import sys
import getopt
#import exceptions
import signal

# supress warning
RPIO.setwarnings(False)

# Which RPIO Numbering you like to use
RPIO.setmode(RPIO.BCM)

# SIG (data from dcf) to SIG to Pin 11 GPIO 17
data_port = 17
data_pin = 11
# ENABLE (the dcf with low) to Pin 7 GPIO 4
enable_port = 4
enable_pin = 7
# LED (show the DCF in as Led) to Pin 18 GPIO 24
led_port = 24
led_pin = 18

# OUT - Enable Port for the module
RPIO.setup(enable_port, RPIO.OUT)
RPIO.gpio_function(enable_port)
RPIO.output(enable_port, RPIO.LOW)

# IN - Read the data
RPIO.setup(data_port, RPIO.IN)

# Globals
datagram = []
debug_level = 0
energy_mode = 0

# ######  define the handler if the program is stopped with ^c ######
# Clean exit!
def clean_exit():
    RPIO.cleanup()
    exit()

# define the handler if the program is stopped with ^c
def handler(signum, frame):
    print ("Catch Error {} - frame :: {}".format(signum, frame))
    clean_exit()

# register the signal handler
signal.signal(signal.SIGINT, handler)
# ------------------------------------------------------------------

# debug info
def pdebug(text):
    if (debug_level == 1):
        print (text)

# Error Exception Handler
# If Bit20 is low
class Bit20Error(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self.args = args
        print("\n-- Error - Bit 20 is LOW - Datagram Error")
# If Bit0 is high
class Bit0Error(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self.args = args
        print("\n-- Error - Bit 0 is HIGH - Datagram Error")
# If Parity was wrong
class ParityBitError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self.args = args
        print("\n-- Error - Parity Bit Error - Datagram Error with " + self.args[0])

# Check the parity bit
def checkParityBit(data_word_type, value_list, parity_bit):
    check = sum(value_list)
    pdebug("-- Parity Check for {0} : Sum {1} : Parity Bit {2}".format(data_word_type, check, parity_bit))
    # the last bit fills up the bit order to a even count
    # even
    if check % 2 == 0:
        if (parity_bit) == 1:
            raise ParityBitError("Error in :: " + data_word_type)
    else:
        if (parity_bit) == 0:
            raise ParityBitError("Error in :: " + data_word_type)

# find the 59 Second with 1000ms low pegel
def get59Seconde():
    print ("-- Wait on 59 Second mark")
    # read the world time
    seconds = time.time()
    sleeptime = 0
    # remember low
    low_time = 0
    low_count = 0
    # remeber high
    high_time = 0
    high_count = 0
    run = True
    found59 = False
    while run:
        # Get act. time
        seconds = time.time()
        # read the port
        if (RPIO.input(data_port)):
            high_count += 1
            high_time = high_time + sleeptime
            low_count = 0
        else:
            low_count += 1
            low_time = low_time + sleeptime
            high_count = 0
        # sleep some milli seconds
        time.sleep(0.01)
        # calculate the time
        sleeptime = time.time() - seconds
        # check for the 59s - full 100 reads low
        # + the minimal low count from the 58 secound 80 ~ 175 to avoid read errors
        # if (low_time > 0.99):
        if ((low_count > 90) and (found59 == False)):
            found59 = True
        # Wait until we found the first HIGH of the 0 Second
        if ((found59) and (high_count == 1)):
            # start with the real decoding
            pdebug("-- Fond the 59second :: PC Time {0} :: High Cnt. {1:2} :: Low Cnt.  {2:2} :: Low time {3:15} :: Sleep time {4:5}".format(datetime.datetime.now().strftime("%H:%M:%S.%f"), high_count, low_count, low_time, sleeptime))
            decode = True
            run = False
    print ("-- ... found")

# Read the datagram
def decodeMinute():
    global datagram
    global energy_mode
    akt_time = 0
    runDecode = True
    aktSecond = 0
    high_count = 0
    low_count = 0
    highDetectedafterReads = 0
    low_time = 0
    high_time = 0
    sleeptime = 0
    seconds = time.time()
    reads = 0
    while runDecode:
        seconds = time.time()
        # read
        if (RPIO.input(data_port)):
            high_count += 1
            high_time = high_time + sleeptime
            # remember after which read count of the act second the pegel was high
            if (highDetectedafterReads < 1):
                highDetectedafterReads = reads
        else:
            low_count += 1
            low_time = low_time + sleeptime
        #Energy Mode - Sleep longer in the midle of the datagramm
        if (energy_mode==1):
            if (reads==30):
                time.sleep(0.59)
                reads=90
        #Normal sleep
        time.sleep(0.01)

        # how long take the sleep
        sleeptime = time.time() - seconds

        # ms of the aktual second
        akt_time = akt_time + sleeptime

        # stop after 1000ms
        if (reads > 95):
            # get the next high count to found the end of the timeframe
            if (RPIO.input(data_port)):
                if (high_count > 20):
                        datagram.append(1)
                else:
                    datagram.append(0)
                printSecDot()
                pdebug("-- Akt Secound {0:2} :: Datagram Time {1:15} :: Reads {2:2}  :: High Cnt. {3:2}  :: Low Cnt. {4:2} :: High time {5:15} :: Low Time  {6:15}  Detect after reads {7:2}".format(aktSecond, akt_time, reads, high_count, low_count, high_time, low_time, highDetectedafterReads))
                # check for valid bits
                # if unvailed raise exception
                # First bit must be alwasy 0
                if (aktSecond == 0):
                    if (datagram[0] == 1):
                        raise Bit0Error
                # Bit 20 always LOW - Start of telegramm
                if (aktSecond == 20):
                    if (datagram[20] == 0):
                        raise Bit20Error
                # check the parity bits of the data words
                if (aktSecond == 28):
                    checkParityBit("MINUTE", datagram[21:28], datagram[28])
                if (aktSecond == 35):
                    checkParityBit("HOUR", datagram[29:35], datagram[35])
                if (aktSecond == 58):
                    checkParityBit("CALENDAR", datagram[36:58], datagram[58])
                #set the defaults
                reads = 0
                akt_time = 0
                high_time = 0
                low_time = 0
                low_count = 0
                high_count = 0
                highDetectedafterReads = 0
                aktSecond += 1
            else:
                reads += 1
        else:
            reads += 1
        if (aktSecond > 58):
            runDecode = False
            # add 59 second
            datagram.append(0)

# get the hour
def getMinuteValue():
    global datagram
    # Check for parity errors
    # check parity bit
    checkParityBit("MINUTE", datagram[21:28], datagram[28])
    minute = datagram[21] * 1 + datagram[22] * 2 + datagram[23] * 4 + datagram[24] * 8 + datagram[25] * 10 + datagram[26] * 20 + datagram[27] * 40
    return minute

def getHourValue():
    global datagram
    # Check for parity errors
    # check parity bit
    checkParityBit("HOUR", datagram[29:35], datagram[35])
    hour = datagram[29] * 1 + datagram[30] * 2 + datagram[31] * 4 + datagram[32] * 8 + datagram[33] * 10 + datagram[34] * 20
    return hour

# get the calendar Values
def getDayValue():
    global datagram
    checkParityBit("CALENDAR", datagram[36:58], datagram[58])
    day = datagram[36] * 1 + datagram[37] * 2 + datagram[38] * 4 + datagram[39] * 8 + datagram[40] * 10 + datagram[41] * 20
    return day
def getWeekDayValue():
    global datagram
    checkParityBit("CALENDAR", datagram[36:58], datagram[58])
    weekday = datagram[42] * 1 + datagram[43] * 2 + datagram[44] * 4
    return weekday
def getMonthValue():
    global datagram
    checkParityBit("CALENDAR", datagram[36:58], datagram[58])
    month = datagram[45] * 1 + datagram[46] * 2 + datagram[47] * 4 + datagram[48] * 8 + +datagram[49] * 10
    return month
def getYearValue():
    global datagram
    checkParityBit("CALENDAR", datagram[36:58], datagram[58])
    year = datagram[50] * 1 + datagram[51] * 2 + datagram[52] * 4 + datagram[53] * 8 + datagram[54] * 10 + datagram[55] * 20 + datagram[56] * 40 + datagram[57] * 80
    return year+2000
#Sommer or Wintertime MEZ or MESZ
def getTimeZoneValue():
    timezone="undef"
    if (datagram[17]==0) and (datagram[18]==1):
        timezone="MEZ"
    if (datagram[17]==1) and (datagram[18]==0):
        timezone="MESZ"
    return timezone
#get at normal date object to set the clock of the server
def getDCF77TimeStamp():
    second = 0
    microsecond = 0
    dcf77_date = datetime.datetime(getYearValue(), getMonthValue(), getDayValue(), getHourValue(), getMinuteValue(), second, microsecond)
    return dcf77_date

#set the OS Date to the right date
def setOSDate(set_date):
    #after the first sucess full read we can set the os clock
    if (set_date==1):
        try:
            new_os_time_str="\"{0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:00\"".format(getYearValue(),getMonthValue(),getDayValue(),getHourValue(),getMinuteValue())
            print ("-- Set the OS Clock with the data string {0} :: Diff {1}".format(new_os_time_str, (datetime.datetime.now()-getDCF77TimeStamp())))
            os.system("date -s " + new_os_time_str + " > /dev/null")
        except:
            print ("-- Unkown error::"), sys.exc_info()
            print ("-- Finish to set OS time to  {0}".format(datetime.datetime.now().strftime("%H:%M:%S.%f")))

# print the dataframe
# for debug purpose on the same line if used in decode function
def printData():
    global datagram
    # print "\r data:: {0}".format(datagram)
    count = 1
    sys.stdout.write("\r-- Datagramm Value::")
    for val in datagram:
        sys.stdout.write(str(val))
        if count == 1:
            sys.stdout.write("-")
        if count == 15:
            sys.stdout.write("-")
        if count == 20:
            sys.stdout.write("-")
        if count == 21:
            sys.stdout.write("-")
        if count == 29:
            sys.stdout.write("-")
        if count == 36:
            sys.stdout.write("-")
        if count == 42:
            sys.stdout.write("-")
        if count == 45:
            sys.stdout.write("-")
        if count == 50:
            sys.stdout.write("-")
        if count == 59:
            sys.stdout.write("-")
        count += 1
    sys.stdout.flush()


# print a dot on the same line
def printSecDot():
    sys.stdout.write(".")
    sys.stdout.flush()


def main(argv):
    global datagram
    global debug_level
    global energy_mode
    set_date=0
    debug_level = 0
    v_runs = 1
    error_count=0
    try:
        opts, args = getopt.getopt(argv, "hr:d:e:s:", ["help=","runs=", "debug=","energymode=","setdate="])
    except getopt.GetoptError:
        print (sys.argv[0] + " -d <debug level 0 to 1> -r <runs> -e <0|1>  -s <0|1>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print (sys.argv[0] + " -d <debug level 0 | 1 > -r <runs> -e < 0 | 1 > -s < 0 | 1 >")
            sys.exit()
        elif opt in ("-r", "--runs"):
            v_runs = int(arg)
        elif opt in ("-d", "--debug"):
            debug_level = int(arg)
        elif opt in ("-e", "--energymode"):
            energy_mode = int(arg)
        elif opt in ("-s", "--setdate"):
            set_date = int(arg)
    print (95 * "-")
    print ("Start Reading the Time Value :: Runs :: {0} :: Debug Level {1} :: Energy Mode {2} :: Set OS Clock {3} ".format(v_runs, debug_level,energy_mode,set_date))

    success_read = False
    #start decode the minutes
    for cyles in range(v_runs):
        #
        #Start to get the start time frame
        print (95 * "=")
        print ("-- Read time data :: run {0}".format(cyles + 1))
        #If we have an read error or start
        #if (success_read==False):
        #find the start of the datagram
        get59Seconde()
        #read
        try:
            print ("-- Start to read the actual Minute Datagram")
            decodeMinute()
            success_read = True
            print ("\n")
        except Bit0Error as error:
            pdebug("-- Bit 0 Error")
            error_count+=1
            success_read = False
        except Bit20Error as error:
            pdebug("-- Bit 20 Error")
            error_count+=1
            success_read = False
        except ParityBitError as error:
            pdebug("-- Parity error")
            error_count+=1
            success_read = False
        except:
            print ("-- Unkown error::"), sys.exc_info()
            success_read = False
            error_count+=1
        #show the datagram
        printData()
        print ("\n")
        # get date only if read was successfull
        if (success_read):
            try:
                print ("-- DCF77 Time     ::{0:02d}:{1:02d} ".format(getHourValue(), getMinuteValue()))
                print ("-- DCF77 Calendar ::{0:02d}.{1:02d}.{2:4d} :: Day of the week {3}".format(getDayValue(),getMonthValue(), getYearValue(), getWeekDayValue()))
                print ("-- DCF77 Timezone ::{0}".format(getTimeZoneValue()))
                print ("-- DCF77 Timestamp::{0}".format(getDCF77TimeStamp()))
                print ("--")
            except ParityBitError as error:
                pdebug("-- Parity error::" + error.args[0])
                error_count+=1
                success_read = False
            except:
                print ("-- Unkown error::"), sys.exc_info()
                error_count+=1
                success_read = False
        #Set now also the date of the server
        if (success_read):
            new_os_time_str_out="\"{0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:00\"".format(getYearValue(),getMonthValue(),getDayValue(),getHourValue(),getMinuteValue())
            #print ("-- Set the OS Clock with the data string {0} :: Diff {1}".format(new_os_time_str, (datetime.datetime.now()-getDCF77TimeStamp())))
            os.system("echo " + str(datetime.datetime.now()) + " " + str(new_os_time_str_out) + " >> /home/pi/dcf77decode.txt")
            setOSDate(set_date)
        # empty list for the next read
        while len(datagram) > 0: datagram.pop()
        success_read = False
        print ("--")
        print ("-- Finish Decode Minute :: OS internal date {0}".format(datetime.datetime.now().strftime("%H:%M:%S.%f")))
    print (80 * "-")
    print ("Finish Reading the Time Value :: Runs :: {0} :: Errors {1}".format(v_runs, error_count))
    print (80 * "-")

# Call Main
if __name__ == "__main__":
    os.system("echo " + str(datetime.datetime.now()) + " > /home/pi/dcf77decode.txt")
    main(sys.argv[1:])

# Clean up
clean_exit()