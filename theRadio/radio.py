#!/usr/bin/python3
#Reference code obtained from "https://www.raspberrypi.org/forums/viewtopic.php?t=53680" by user: LinuxCircle
import smbus as smbus 
import subprocess
import curses
import curses.textpad
import time

i2c = smbus.SMBus(1) # newer version RASP (512 megabytes)
i2c_address = 0x60

def init_radio(address):
    """initialize hardware"""
    i2c.write_quick(address)
    time.sleep(0.1)


def set_freq(address, freq):
    """set Radio to specific frequency"""
    freq14bit = int (4 * (freq * 1000000 + 225000) / 32768) # Frequency distribution for two bytes (according to the data sheet)
    freqH = freq14bit>>8 #int (freq14bit / 256)
    freqL = freq14bit & 0xFF

    data = [0 for i in range(4)] # Descriptions of individual bits in a byte - viz.  catalog sheets
    init = freqH # freqH # 1.bajt (MUTE bit; Frequency H)  // MUTE is 0x80
    data[0] = freqL # 2.bajt (frequency L)
    data[1] = 0xB0 #0b10110000 # 3.bajt (SUD; SSL1, SSL2; HLSI, MS, MR, ML; SWP1)
    data[2] = 0x10 #0b00010000 # 4.bajt (SWP2; STBY, BL; XTAL; smut; HCC, SNC, SI)
    data[3] = 0x00 #0b00000000 # 5.bajt (PLREFF; DTC; 0; 0; 0; 0; 0; 0)
    try:
      i2c.write_i2c_block_data (address, init, data) # Setting a new frequency to the circuit
      print("Frequency set to: " + str(freq))
    except IOError:
      subprocess.call(['i2cdetect', '-y', '1'])


def mute(address):
    """"mute radio"""
    freq14bit = int(4 * (0 * 1000000 + 225000) / 32768)
    freqL = freq14bit & 0xFF
    data = [0 for i in range(4)]
    init = 0x80
    data[0] = freqL
    data[1] = 0xB0
    data[2] = 0x10
    data[3] = 0x00
    try:
        i2c.write_i2c_block_data(address, init, data)
        print("Radio Muted")
    except IOError:
        subprocess.call(['i2cdetect', '-y', '1'])


if __name__ == '__main__':
    init_radio(i2c_address)
    frequency = 101.1 # sample starting frequency
    # terminal user input infinite loop
    stdscr = curses.initscr()
    curses.noecho()
    try:
        while True:
            c = stdscr.getch()
            if c == ord('f'): # set to 101.1
                frequency = 101.1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('v'): # set to 102.1
                frequency = 102.1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('w'): # increment by 1
                frequency += 1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('s'): # decrement by 1
                frequency -= 1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('e'): # increment by 0.1
                frequency += 0.1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('d'): # decrement by 0.1
                frequency -= 0.1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('m'): # mute
                mute(i2c_address)
                time.sleep(1)
            elif c == ord('u'): # unmute
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('q'): # exit script and cleanup
                mute(i2c_address)
                curses.endwin()
                break
    except KeyboardInterrupt:
        mute(i2c_address)
        curses.endwin()
