#!/usr/bin/python3
version=185

# pip3 install --upgrade versioneer https://github.com/warner/python-versioneer
# pip3 install --upgrade versioneer2

# remote debug  https://electrobotify.wordpress.com/2019/08/16/remote-development-on-raspberry-pi-with-vs-code/
#               https://code.visualstudio.com/docs/remote/ssh
#               https://code.visualstudio.com/docs/python/debugging
#               https://www.raspberrypi.org/blog/coding-on-raspberry-pi-remotely-with-visual-studio-code/
# https://www.internetradio-horen.de/radio/baden-wurttemberg

modulname='janradio'
# to better debug: on crash enter: import pdb; pdb.pm()
# check allocated memory: ps --sort -rss -eo rss,pid,command | head
# sudo apt-get remove -y libuim0 libuim0-nox uim-common
import datetime
import os
import pathlib
import socket
import subprocess
#
import sys
import importlib.util #pip3 install --upgrade importlib
import threading
import time  # , struct, datetime
import timeit

#import fontconfig
#import fontTools
#from fontTools import ttLib
#import fontTools.ttLib
########################################################################################
import tkinter
import traceback
import urllib
from tkinter import font, ttk
from urllib import parse

import PIL  #sudo apt-get install python3-pil.imagetk  or  pip3 install pillow  or  python -m pip install pillow
#   import queue as queue
#   from multiprocessing import Queue
import psutil
#import resource
#subprocess.Popen(['omxplayer','-b',os.path.join(path_aNixie,'shutdown.wav')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
#https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.get_length
import pygame
#import re
##################################
import requests as requests
from PIL import ImageTk

#import urllib.parse
#from urllib.parse import urlsplit, urlunsplit
##################################
import jksip as jksip
import jksmeter360 as meter360
import jksmetermg as metermg
import jksmeterva as meterva
import jksnixieclock as nixieclock

#sudo pkill -SIGKILL -f "python3" > /dev/null 2>&1
#"omxplayer -o local /home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4"
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/Electronics_At_Work_1943_Part_3.mp4' --win '0 0 248 180' --no-osd
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '0 0 800 480'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 992 720'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 496 360'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 248 180'
# omxplayer -o local 'http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
# omxplayer -o hdmi 'https://youtu.be/YtPSa4LTWgo'
# DISPLAY=:0 /usr/bin/lxterminal -e mplayer '/mnt/c/Users/janka_cg1/Dropbox/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
# DISPLAY=:0 /usr/bin/lxterm -e mplayer '/mnt/c/Users/janka_cg1/Dropbox/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
# DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
# DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/Music/Asaf Avidan - One Day Live @ Sziget 2015.mp3'
global the_hostname
the_hostname = socket.gethostname()
global sound_exist
sound_exist = 0
global sound_out_type
sound_out_type = 'local'
global gpio_exist
gpio_exist = 0
global printredirect
printredirect = 0
global trafic_stat_old
trafic_stat_old = 0
global trafic_stat_show
trafic_stat_show = 0

#https://docs.python.org/3/library/pathlib.html
#if sys.platform == "win32":
#    import ntpath
#    pathmodule = ntpath
#else:
#    import posixpath
#    pathmodule = posixpath
#print ('jk-pathmodule: %s' % str(pathmodule))
##########################################################################
# # https://pi-buch.info/raspbian-stretch/
# gpiozero oder pigpio via: 
# # https://gpiozero.readthedocs.org/en/rest-docs/
# # python -m pip install gpiozero
# # sudo apt-get install python-gpiozero python3-gpiozero

# check if 
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

if ('pi4radio1' in the_hostname or 'pi4radio2' in the_hostname):
    sound_out_type = 'hdmi'

try:
    # Check and import real RPi.GPIO library
    importlib.util.find_spec('RPi.GPIO') # sudo apt install -y python3-rpi.gpio
    import RPi.GPIO as GPIO # sudo apt install -y python3-rpi.gpio
    GPIO.setmode(GPIO.BCM)# GPIO.BOARD)
    GPIO.cleanup()
    gpio_exist=1
except Exception as e:
    print ("jk-import RPi.GPIO failed, Exception as e:")
    print (e)
except ImportError:
    # If real RPi.GPIO library fails, load one of the fake one
    # import FakeRPi.RPiO as RPiO
    # or
    import FakeRPi.GPIO as GPIO
    # # ## pip install git+https://github.com/sn4k3/FakeRPi
    # # ## pip3 install --upgrade git+https://github.com/sn4k3/FakeRPi
except:
    print ("jk-import RPi.GPIO failed, traceback:")
    traceback.print_exc()
###########################################################################
if __name__ == '__main__':
    print ('janradiogrid: in main')
    root = tkinter.Tk()
    if not sys.platform == "win32":
        os.system('pkill omxplayer')
    if not ('sky' in the_hostname or 'test' in the_hostname):
        root.overrideredirect(1)
        root.wm_attributes("-topmost", True)
##        root.wm_attributes("-alpha", 0.5)
##        root.wm_attributes("-disabled", True)
##        root.wm_attributes("-transparentcolor", "blue")
##        root.withdraw()
##        root.wm_attributes("-toolwindow", 1)
##        root.update_idletasks()
#root.tk_setPalette(background='#40E0D0', foreground='black',activeBackground='black', activeForeground='yellow')
########################################################################################
global Beschriftungen
Beschriftungen = ['Empfänger', 'Sender', 'Betrieb', 'Kanal', 'Wellenanzeiger', 'Netzanode', 'Frequenzkontrolle', 
                  'Sichtgerät', 'Antennen Abstimmung', 'Antennen Kopplung', 'Taste', 'Vorheizen',
                  'Verkehrsart', 'Mithören', 'Ortstaste', 'Fernhörer', 'Modulation',
                  'Leistung', 'Laustärke','Aus','Ein', 'Grob', 'Fein', 'Hauptschalter']


global path_script
path_script = sys.path[0]
if not os.path.isdir(path_script):
    sys.exit()
if not pathlib.Path(path_script).exists:
    sys.exit()
if not pathlib.Path(path_script).is_dir:
    sys.exit()
path_aGauge = os.path.join(path_script,'aGauge')
path_aNixie = os.path.join(path_script,'aNixie')
path_bImages = os.path.join(path_script,'bImages')
path_aFrame = os.path.join(path_script,'aFrame')
path_aSound = os.path.join(path_script,'aSound')
path_aMagicEye = os.path.join(path_script,'aMagicEye')
path_file_senders = os.path.join(path_script, 'senderlist.txt')
path_file_sender = os.path.join(path_script, 'sender.txt')
path_file_temp = os.path.join(path_script, 'temp_' + the_hostname + '_2.txt')
charging_trueImage = tkinter.PhotoImage(os.path.join(path_bImages,'button_true_105x42.png'))
charging_trueImagePIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_bImages,'button_true_105x42.png'))
charging_falseImage = tkinter.PhotoImage(os.path.join(path_bImages,'button_false_105x42.png'))
charging_falseImagePIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_bImages,'button_false_105x42.png'))
###########################################################################
def replace_at(temp_string):
    try:
        filetosearch = '/home/ubuntu/ip_table.txt'
        texttoreplace = 'tcp443'
        texttoinsert = 'udp1194'
        s = open(filetosearch).read()
        s = s.replace(texttoreplace, texttoinsert)
        f = open(filetosearch, 'w')
        f.write(s)
        f.close()
        quit()
        print ("jk-did print_to to file: %s" % path_file_temp)
        return 0
    except:
        traceback.print_exc()
        print ("jk-could not print_to to file: %s" % path_file_temp)
        return 1
def print_to(temp_string):
    try:
        with open(path_file_temp,"a") as temp_file:
            temp_file.write(temp_string + "\n")
            print ("jk-did print_to to file: %s" % path_file_temp)
            return 0
    except:
        traceback.print_exc()
        print ("jk-could not print_to to file: %s" % path_file_temp)
        return 1

if printredirect:
    print ('jk-path_file_temp is %s' % path_file_temp)
    with open(path_file_temp,"w") as ctemp_file: ctemp_file.write(str(datetime.datetime.now())+"\n")
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    #fh = open("output.txt","w")
    #fh = open("errors.txt","w")
    fh = open(path_file_temp,"w")
    sys.stdout = fh
    sys.stderr = fh
    print ('jk-This first line ist print to file') #,end=" :-) " #,sep=" :-) "
#print ('jk-printing to stdout', file=sys.stdout)
#print ('jk-printing to stderr', file=sys.stderr)
print ('jk-hostname: %s' % str(the_hostname))
print ('jk-platform: %s' % str(sys.platform))
print ('jk-Python version: %s' % str(sys.version))
#print ('jk-Python version_info: %s' % str(sys.version_info))
print ('jk-Python executable: %s' % str(sys.executable))
print ('jk-Python path: %s' % str(sys.path))
#sys.path.append("/path/to/my/module")
#print ("jk-Python modules: %s" % str(sys.modules))
print ('jk-path_script is %s' % path_script)
#sys.stdout.write
#print ("jk-Python __stdin__: %s" % sys.__stdin__)
#print ("jk-Python __stdout__: %s" % sys.__stdout__)
#print ("jk-Python __stderr__: %s" % sys.__stderr__)
#print ("jk-Python displayhook : %s" % sys.displayhook)
###########################################################################
def process_start_radio(radio_station):
    #todo http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_GPIO_int.html
    print ('  play: "%s"' % (radio_station))
    if not sys.platform == "win32":
        try:
            #omxc = subprocess.Popen(['omxplayer', '-o','hdmi', radio_station,'&'])
            omxc = subprocess.Popen(['omxplayer', '-o', sound_out_type, radio_station,'&'])

            hdmic = subprocess.Popen(['vcgencmd', 'display_power', '1','&'])
            return True
        except:
            traceback.print_exc()
        if not (str(sender_key.get('state')) == '1'):
            try:
                os.system('mplayer -quiet -cache 100 ' + radio_station + ' &')
                return True
                #omxc = subprocess.Popen('mplayer -quiet -cache 100 ' + dicsenders.get(list_value) + ' &')
                #mswr1bw='mplayer -quiet -cache 100 http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                #swr1bw='omxplayer -o local http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                #swr1bw='omxplayer -o hdmi http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                #omxplayer --win '100 100 500 500'
                #vcgencmd display_power 1
                #https://github.com/cmus/cmus/wiki/status-display-programs
                #'cmus http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                #https://opensource.com/life/16/8/3-command-line-music-players-linux
            except:
                traceback.print_exc()
        if 0==1:
            #ps = subprocess.Popen(['omxplayer', '-o','hdmi', radio_station], shell=True, stdout=subprocess.PIPE)
            ps = subprocess.Popen(['omxplayer', '-o',sound_out_type, radio_station], shell=True, stdout=subprocess.PIPE)
            ps_pid = ps.pid
            output = ps.stdout.read()
            ps.stdout.close()
            ps.wait()
    else:
        try:
            os.system('start wmplayer "' + radio_station + '"')
            return True
        except:
            traceback.print_exc()
    return False
def process_stop_radio():
    print('   stop radio')
    if not sys.platform == "win32":
        #print('pkill omxplayer')
        os.system('pkill omxplayer')
        #print('pkill mplayer')
        os.system('pkill mplayer')
    else:
        #print('TASKKILL wmplayer')
        os.system('TASKKILL /F /IM wmplayer.exe')
        #os.system("taskkill python* && python D:\__Dropbox\Dropbox\aRadio\theRadio\janradiogrid.py"
def process_exists(proc_name):
    proclist = psutil.process_iter()
    for proc in proclist:
        the_proc_name = ''
        the_proc_name = proc.name()
        the_proc_state = psutil.STATUS_ZOMBIE
        the_proc_state = proc.status()
        if proc_name in the_proc_name and (the_proc_state == psutil.STATUS_RUNNING or the_proc_state == psutil.STATUS_SLEEPING):
            return True
    return False
def get_sys_class(sys_class_string='/sys/class/thermal/thermal_zone0/temp'):
    tempC = 21
    if (('rpi' in socket.gethostname()) or ('radio' in socket.gethostname())):
        if '/sys/class/thermal/thermal_zone0/temp' in sys_class_string:
            tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
        else:
            tempC = int(open(sys_class_string).read())
    return tempC
def get_bandwidh(interface='wlan0',direction='rx'):
    tempB = 21
    if (('rpi' in socket.gethostname()) or ('radio' in socket.gethostname())):
        tempr1 = int(open('/sys/class/net/' + interface + '/statistics/rx_bytes').read())
        tempt1 = int(open('/sys/class/net/' + interface + '/statistics/tx_bytes').read())
        time.sleep(1)
        tempr2 = int(open('/sys/class/net/' + interface + '/statistics/rx_bytes').read())
        tempt2 = int(open('/sys/class/net/' + interface + '/statistics/tx_bytes').read())
        tempr = tempr2 - tempr1
        tempt = tempt2 - tempt1
        if ('rx' in direction):
            tempB = tempr
        elif ('tx' in direction):
            tempB = tempt
        else:
            tempB = tempr + tempt
    return tempB
def get_sys_class_string(sys_class_string='/proc/cpuinfo'):
    tempC = '21'
    if (('rpi' in socket.gethostname()) or ('radio' in socket.gethostname())):
        tempC = str(open(sys_class_string).read())
    return tempC
##    if not sys.platform == "win32":
##        ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
##        ps_pid = ps.pid
##        output = ps.stdout.read()
##        ps.stdout.close()
##        ps.wait()
##        for line in output.split("\n"):
##            res = re.findall("(\d+) (.*)", line)
##            if res:
##                pid = int(res[0][0])
##                if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
##                    return True
##        return False
##    else:
##        #if proc_name in (p.name() for p in psutil.process_iter()):
##        for p in psutil.process_iter():
##            if proc_name in (p.name()):
##                print (p.name())
##                return True
##        return False
##            os.system("sudo pkill -f omxplayer* && sudo pkill -f python* && python3 /home/pi/aRadio/theRadio/janradiogrid.py")
##            #os.system('sudo shutdown -r now')
##            #os.system('sudo reboot')
##            os.system("sudo reboot > /dev/null 2>&1")
print ("my_cpu_temp:%d" % get_sys_class())
def button1aclick():
    print ('  button1aclick' )
    button1a.configure(image=charging_falseImagePIL)
    #button1a.bell()
    exitfunc()
def button1bclick():
    print ('  button1bclick' )
    button1b.configure(image=charging_falseImagePIL)
    #button1b.bell()
def button3aclick(ButtonAnAus=18):
    print ('  button3aclick' )
    #button3a.bell()
    #process_stop_radio()
    #if 1 == button1bpressed.get():
    #utton1bpressed.set(0)
    if (str(sender_key.get('state')) == '1'):
        print ('  ---------------state running - we stop now')
        process_stop_radio()
        set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'0' )
    else:
        print ('  ---------------state stoped - we start now')
        process_stop_radio()
        process_start_radio(dicsenders.get(str(sender_key.get('last'))))
        set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'1' )
    t3b.delete('1.0', tkinter.END)
    t3b.insert(tkinter.END, "JK Radio (2018) V:%s" % str(version),'JK')
    #t3b.delete("end-1c linestart", tkinter.END)
    t3b.insert(tkinter.END, '\n' + dicsendershost.get(str(sender_key.get('last'))), 'STATE')
    #t3b.insert("%d.%d" % (2, 0), '\n' + dicsendershost.get(list_value), 'STATE')
    if str(sender_key.get('state')) == '1':
        t3b.tag_config('STATE', foreground='green')
    elif str(sender_key.get('state')) == '0':
        t3b.tag_config('STATE', foreground='red')
    else:
        t3b.tag_config('STATE', foreground='yellow')
    time.sleep(1)
    if not sys.platform == "win32":
        if process_exists('omxplayer') or process_exists('mplayer'):
            #button3apressed.set(1)
            button3a.configure(image=charging_trueImagePIL)
        else:
            #button3apressed.set(0)
            button3a.configure(image=charging_falseImagePIL)
    else:
        if process_exists('wmplayer'):
            #button3apressed.set(1)
            button3a.configure(image=charging_trueImagePIL)
        else:
            #button3apressed.set(0)
            button3a.configure(image=charging_falseImagePIL)
##########################
def exit(event):
    print ('jk-This exit')
    exitfunc()
def on_closing():
    print ('jk-This on_closing')
    exitfunc()
def exitfunc():
    process_stop_radio()
    if sound_exist==1:
        effect_shutdown.play()
        while pygame.mixer.get_busy() == True:
        #while pygame.mixer.music.get_busy() == True:
            continue
    if gpio_exist == 1:
        GPIO.cleanup(dt)
        GPIO.cleanup(clk)
    if printredirect:
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout = save_stdout
        sys.stderr = save_stderr
        fh.close()
    print ('jk-This last via exitfunc 1')
    root.quit()
    print ('jk-This last via exitfunc 2')
    #quit()
    print ('jk-This last via exitfunc 3')
    #sys.exit() #exit with exception, used to exit treads
    #root.destroy()
sys.exitfunc = exitfunc
root.bind("<Escape>", exit)
########################################################################################
#try:
#    unicode = unicode
#except NameError:
#    str = str
#    unicode = str
#    bytes = bytes
#    basestring = (str,bytes)
#    print ("unicode is undefined, must be Python 3")
#else:
#    str = str
#    #unicode = unicode
#    #bytes = str
#    #basestring = basestring
#    print ("jk-unicode exists, must be Python 2")
global global_font
appHighlightFont = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
tkinter.font.families()
helv36 = tkinter.font.Font(family="Helvetica",size=36,weight="bold")
#helv36 = ("Helvetica", 36, "bold")
nixie12 = tkinter.font.Font(family="Nixie One",size=12,weight="bold")
nixie18 = tkinter.font.Font(family="Nixie One",size=18,weight="bold")
nixie24 = tkinter.font.Font(family="Nixie One",size=24,weight="bold")
nixie36 = tkinter.font.Font(family="Nixie One",size=36,weight="bold")
#nixie24 = ("Nixie One", 24, "bold")
#global_font=("1952 RHEINMETALL", 22, "bold")
global_font = nixie24

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1
def shortName( font ):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font['name'].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')
        else:
            try:
                name_str = record.string.decode('utf-8')
            except UnicodeDecodeError:
                traceback.print_exc()
                name_str = record.string.decode('latin-1')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            family = name_str
        if name and family: break
    return name, family
#print ("jk-font helv36 name: %s" % str(shortName( helv36 )))
#print ("jk-font Nixie name: %s" % str(shortName( nixie24 )))
###########################################################################
###########################################################################
print ("jk-----------------------------------------------------------6")
#https://serverfault.com/questions/709546/how-to-get-local-ip-address-associated-with-default-gateway
x = jksip.JKSIP(1)
print ("Number of instances: : " + str(jksip.JKSIP.counter))
y = jksip.JKSIP(2)
print ("Number of instances: : " + str(jksip.JKSIP.counter))
del x
print ("Number of instances: : " + str(jksip.JKSIP.counter))
del y
print ("Number of instances: : " + str(jksip.JKSIP.counter))

global ip_internal
ip_internal = jksip.JKSIP(1).get_ip_internal()
print ('ip_internal: %s' % str(ip_internal))
global ip_gateway
ip_gateway = jksip.JKSIP(1).get_ip_gateway()
print ('jk-gateway: %s' % ip_gateway)
global ip_sender
ip_sender = 'snakekiller.de'
global time_sender
time_sender = 900
print ("jk-----------------------------------------------------------7")
#jk-screen width:480 height:320
#jk-screen width:1280 height:1024
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print ("jk-screen winfo_screen width:%d  height:%d" % (screen_width,screen_height))
sizex = 800
sizey = 480
posx  = 0
posy  = 0
taskbar_height = 0

if screen_width < sizex:
    sizex = screen_width
if screen_height < sizey:
    sizey = screen_height
if screen_height > 800:
    taskbar_height = 40
if (not 'rpi' in the_hostname):
    taskbar_height = 100
if (screen_height - taskbar_height > sizey):
    posy  = screen_height - taskbar_height - sizey

#def get_screen_size(display):
#    mon_geoms = [
#        display.get_monitor(i).get_geometry()
#        for i in range(display.get_n_monitors())
#    ]
#    x0 = min(r.x            for r in mon_geoms)
#    y0 = min(r.y            for r in mon_geoms)
#    x1 = max(r.x + r.width  for r in mon_geoms)
#    y1 = max(r.y + r.height for r in mon_geoms)
#    return x1 - x0, y1 - y0
def get_screen_size_width(display):
    mon_geoms = [
        display.get_monitor(i).get_geometry()
        for i in range(display.get_n_monitors())
    ]
    x0 = min(r.x            for r in mon_geoms)
    x1 = max(r.x + r.width  for r in mon_geoms)
    return x1 - x0
def get_screen_size_height(display):
    mon_geoms = [
        display.get_monitor(i).get_geometry()
        for i in range(display.get_n_monitors())
    ]
    y0 = min(r.y            for r in mon_geoms)
    y1 = max(r.y + r.height for r in mon_geoms)
    return y1 - y0
    
try:
    # https://developer.gnome.org/gdk3/stable/GdkScreen.html
    import gi
    gi.require_version('Gdk', '3.0')
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gdk, Gtk, GObject

    # example use
    #print ("jk-screen Display both:")
    #print(get_screen_size(Gdk.Display.get_default()))
    print (" ################################# ")
    print ("jk-screen Display       width:%d  height:%d" % (get_screen_size_width(Gdk.Display.get_default()),get_screen_size_height(Gdk.Display.get_default())))

    #s = Gdk.Screen.get_default()
    #print ("jk-screen Screen       width:%d  height:%d" % (s.get_width(),s.get_height()))
    # Replace w with the GtkWindow of your application
    #w = Gtk.Window()
    # Get the screen from the GtkWindow
    #s = w.get_screen()
    # Using the screen of the Window, the monitor it's on can be identified
    #m = s.get_monitor_at_window(s.get_active_window())
    # Then get the geometry of that monitor
    #monitor = s.get_monitor_geometry(m)
    # This is an example output
    #print ("jk-screen Monitor      width:%s  height:%s" % (monitor.width, monitor.height))
    #w.maximize()
    #themaxsize = w.get_size()
    #print ("jk-screen Windows      maxwidth:%s  maxheight:%s" % (themaxsize.width, themaxsize.height))

except:
    print ("jk-screen import gi failed")
    traceback.print_exc()

print ("jk-screen app size     width:%d  height:%d" % (sizex,sizey))
root.geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
#root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))#root.geometry("400x400+100+100")
print ("jk-----------------------------------------------------------9")
root.configure(background='black')
root.title("unbekannt via %s" % ip_gateway + ' v:' + str(version))
####################################################################
#http://effbot.org/tkinterbook/widget.htm
#http://effbot.org/tkinterbook/tkinter-hello-again.htm
#http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
#https://www.python-kurs.eu/tkinter_canvas.php
#http://www.tkdocs.com/tutorial/grid.html
#http://effbot.org/tkinterbook/grid.htm
#allways try to change:
#           Button(frame, text="Hello", command=self.hello).pack(side=LEFT)
#to this two lines:
#           w = Button(frame, text="Hello", command=self.hello)
#           w.pack(side=LEFT)
#root.protocol("WM_DELETE_WINDOW", on_closing)
###########################################################################
time1 = ''
def tick():
##    global time1
##    # get the current local time from the PC
##    time2 = time.strftime('%H:%M:%S')
##    # if time string has changed, update it
##    if time2 != time1:
##        time1 = time2
##        clock.config(text=time2)
##    # calls itself every 200 milliseconds
##    # to update the time display as needed
##    # could use >200 ms, but display gets jerky
    #localtime = time.asctime( time.localtime(time.time()) )
    #print ("Local current time: %s" % str(localtime))
    #s = time.strftime('%H:%M:%S')
    s = time.strftime('%H:%M')
    if s != clock["text"]:
        clock["text"] = s
    clock.after(10000, tick)
def ticker():
##    global time1
##    # get the current local time from the PC
##    time2 = time.strftime('%H:%M:%S')
##    # if time string has changed, update it
##    if time2 != time1:
##        time1 = time2
##        clock.config(text=time2)
##    # calls itself every 200 milliseconds
##    # to update the time display as needed
##    # could use >200 ms, but display gets jerky
    #localtime = time.asctime( time.localtime(time.time()) )
    #print ("Local current time: %s" % str(localtime))
    #s = time.strftime('%H:%M:%S')
    #s = time.strftime('%H:%M')
    #if s != clock["text"]:
    #    clock["text"] = s
    h = int(time.strftime('%H'))
    m = int(time.strftime('%M'))
    s = 0
    setclockdaytime(h,m,s)
    clock_nixieclock.after(1000, ticker)
#https://docs.python.org/3.5/library/tkinter.ttk.html?highlight=ttk
tkkstyle = 0
style = tkinter.ttk.Style() #use it as style="BW.TLabel")
style.configure("BW.TLabel"
                #, foreground="white"
                #, background="black"
                )
#borderwidth=0,highlightthickness=0

clock_nixieclock = nixieclock.Clock(root,width=440,height = 220) #,borderwidth=0,highlightthickness=0)
#clock_nixieclock.grid(row=2, column=0,sticky = "nsew")
clock_nixieclock.place(x=0, y=0)    #, relwidth=1, relheight=1 ,anchor="nw")
#clock_nixieclock.configure(borderwidth=0,highlightthickness=0)
#clock_nixieclock.set(0)

global meter1
meter1=3
if meter1==1:
    meter1_metermg = metermg.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
    meter1_metermg.setrange(0,100)
    meter1_metermg.place(x=0, y=220)
elif meter1==2:
    meter1_meter360 = meter360.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
    meter1_meter360.setrange(0,100)
    meter1_meter360.place(x=0, y=220)
elif meter1==3:
    meter1_meterva = meterva.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
    meter1_meterva.setrange(0,100,typetxt='cpu')
    meter1_meterva.place(x=0, y=220)

global meter2
meter2=3
if meter2==1:
    meter2_metermg = metermg.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
    meter2_metermg.setrange(0,150)
    meter2_metermg.place(x=220, y=220)
elif meter2==2:
    meter2_meter360 = meter360.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
    meter2_meter360.setrange(0,150)
    meter2_meter360.place(x=220, y=220)
elif meter2==3:
    meter2_meterva = meterva.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
    meter2_meterva.setrange(0,150,typetxt='ms')
    meter2_meterva.place(x=220, y=220)
##############################################            
btframe1 = tkinter.Frame(root,width=220,height = 40)#,borderwidth=0,highlightthickness=0,relief=tkinter.FLAT,background='green')
##btframe1.grid(row=0, column=0, rowspan = 2,columnspan = 2,sticky = "nsew")
btframe1.place(x=0, y=440
                        #, relwidth=1, relheight=1
                        #,anchor="s"
                        )

t1a = tkinter.Text(btframe1 , background='black',foreground='orange',borderwidth=0,highlightthickness=0
                    #,exportselection=0
                        #,relief=tkinter.FLAT
                        #,relief=tkinter.RAISED
                        #,relief=tkinter.SUNKEN
                        #,relief=tkinter.GROOVE
                        #,relief=tkinter.RIDGE       
##                        ,selectmode=tkinter.SINGLE
##                        ,foreground='saddle brown'
##                        ,selectforeground='orange'
##                        ,selectbackground='orange'
                        #,highlightcolor='saddle brown'
                        #,highlightbackground='sandy brown'
##                        ,highlightthickness=5
##                        ,disabledforeground='red'
                    #,width=110
                    #,height=2
                    #,padx=5
                    #,pady=2
                    )
#t1a.insert(tkinter.END, "JK Radio 1a")
t1a.place(x=0, y=0)
#t1a.pack(side=tkinter.LEFT ,fill=tkinter.Y , expand=tkinter.YES  )
#var=0
button1apressed = tkinter.IntVar()
#button1a = tkinter.Checkbutton(t1a
                               #, variable=var
                               #, indicatoron=0
button1a = tkinter.Button(t1a
                          , text="Beenden"
                          #, font=nixie12
                          , font=tkinter.font.Font(family="Nixie One",size=11,weight="bold")
                          , padx=5
                          #, pady=10
                          ,height=35
                          #, width=15
                          #,anchor='w'
                          #, justify=tkinter.LEFT
                          ,relief=tkinter.RAISED
                          ,background='black',foreground='orange',borderwidth=0,highlightthickness=0
                          ,highlightcolor='orange'
                          ,highlightbackground='orange'
                          ,disabledforeground='red'
                          ,compound=tkinter.CENTER
                          ,image=charging_trueImagePIL
                          ,command=button1aclick)
t1a.window_create(tkinter.INSERT, window=button1a)



t1b = tkinter.Text(btframe1 , background='black',foreground='orange',borderwidth=0,highlightthickness=0
                    #,exportselection=0
                    ,relief=tkinter.FLAT
                    #,width=110
                    #,height=2
                    #,padx=5
                    #,pady=2
                    )
#t1b.insert(tkinter.END, "JK Radio 1b")
t1b.place(x=110, y=0)
#t1b.pack(side=tkinter.LEFT,fill=tkinter.Y, expand=tkinter.YES)
#var=0
button1bpressed = tkinter.IntVar()
button1b = tkinter.Checkbutton(t1b
                               ,variable=button1bpressed
                               ,indicatoron=0
#button1b = tkinter.Button(t1b
                          , text="CPU/Tmp"
                          #, font=nixie12
                          , font=tkinter.font.Font(family="Nixie One",size=11,weight="bold")
                          , padx=5
                          #, pady=10
                          ,height=35
                          #, width=15
                          #,anchor='n'
                          #, justify=tkinter.LEFT
                          ,relief=tkinter.RAISED
                          ,background='black',foreground='orange',borderwidth=0,highlightthickness=0
                          ,highlightcolor='orange'
                          ,highlightbackground='orange'
                          ,disabledforeground='red'
                          ,compound=tkinter.CENTER
                          ,image=charging_falseImagePIL
                          ,command=button1bclick                               )
t1b.window_create(tkinter.INSERT, window=button1b)



######
btframe2 = tkinter.Frame(root,width=220,height = 40,borderwidth=0,highlightthickness=0) #, relief=tkinter.RAISED,background='red')
##btframe1.grid(row=0, column=0, rowspan = 2,columnspan = 2,sticky = "nsew")
btframe2.place(x=220, y=440
                        #, relwidth=1, relheight=1
                        #,anchor="e"
                        )
t2a = tkinter.Text(btframe2, background='black',foreground='orange',borderwidth=0,highlightthickness=0
                    #,exportselection=0
                    ,relief=tkinter.SUNKEN
                    #,width=110
                    #,height=2
                    #,padx=5
                    #,pady=2
                    )
#https://pypi.python.org/pypi/psutil
t2a.delete(1.0, tkinter.END)
t2a.insert(tkinter.END, str(get_sys_class_string('/proc/cpuinfo')))
t2a.place(x=0, y=0)
#t2a.pack(side=tkinter.LEFT ,fill=tkinter.Y , expand=tkinter.YES  )
############
btframe3 = tkinter.Frame(root,width=360,height = 40,borderwidth=0,highlightthickness=0) #, relief=tkinter.RAISED,background='red')
##btframe1.grid(row=0, column=0, rowspan = 2,columnspan = 2,sticky = "nsew")
btframe3.place(x=440, y=440
                        #, relwidth=1, relheight=1
                        #,anchor="e"
                        )
t3a = tkinter.Text(btframe3, background='black',foreground='orange',borderwidth=0,highlightthickness=0
                    #,exportselection=0
                    ,relief=tkinter.SUNKEN
                    #,width=110
                    #,height=2
                    #,padx=5
                    #,pady=2
                    )
#t3a.insert(tkinter.END, "JK Radio 3a")
t3a.place(x=0, y=0)
#t3a.pack(side=tkinter.LEFT ,fill=tkinter.Y , expand=tkinter.YES  )
#button3apressed = tkinter.IntVar()
#button3a = tkinter.Checkbutton(t3a
#                               ,variable=button3apressed
#                               ,indicatoron=0
button3a = tkinter.Button(t3a
                          ,text="An / Aus"
                          #, font=nixie12
                          , font=tkinter.font.Font(family="Nixie One",size=11,weight="bold")
                          , padx=5
                          #, pady=10
                          ,height=35
                          #, width=15
                          #,anchor='n'
                          #, justify=tkinter.LEFT
                          ,relief=tkinter.RAISED
                          ,background='black',foreground='orange',borderwidth=0,highlightthickness=0
                          ,highlightcolor='orange'
                          ,highlightbackground='orange'
                          ,disabledforeground='red'
                          ,compound=tkinter.CENTER
                          ,image=charging_falseImagePIL
                          ,command=button3aclick)
t3a.window_create(tkinter.INSERT, window=button3a)

t3b = tkinter.Text(btframe3, background='black',foreground='orange',borderwidth=0,highlightthickness=0
                    #,exportselection=0
                    ,relief=tkinter.SUNKEN
                    #,width=220
                    #,height=2
                    #,padx=5
                    #,pady=2
                    )
t3b.insert("%d.%d" % (1, 0), "JK Radio (2018) V:%s" % str(version),'JK')
#t3b.insert("%d.%d" % (1, 0), "JK V:%s\n" % str(version),'JK')
t3b.insert("%d.%d" % (2, 0), "\nSender unbekannt", 'STATE')
t3b.tag_config('STATE', foreground='yellow')
t3b.place(x=110, y=0)
#t3b.pack(side=tkinter.LEFT,fill=tkinter.Y, expand=tkinter.YES)
##t3b.insert(tkinter.END, "JK Radio 3b")
##t3b.insert('insert', ' red text', 'RED')
##t3b.tag_config('RED', foreground='red')

#######################################################################################################################
#http://code.activestate.com/recipes/580782-image-background-for-tkinter/
#backgroundImageMid = tkinter.PhotoImage(os.path.join(path_aFrame,'template_440x440.png'))
backgroundImageMidPIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_aFrame,'template_360x440.png'))
imagelabelmid = tkinter.Label(root,width=360,height = 440,borderwidth=0,highlightthickness=0,image = backgroundImageMidPIL)
imagelabelmid.place(x=440, y=0,
                    #relwidth=1, relheight=1
                    #,anchor="nw"
                    )
#imagelabelmid.grid(row=0, column=3,sticky = "nsew")
imagelabelmid.image = backgroundImageMidPIL

#imagelabel = tkinter.Label(rightmidframe,width=440,height = 440,borderwidth=0,highlightthickness=0)
#imagelabel.configure(image=backgroundImage2)
#imagelabel.grid(row=1, column=0,rowspan = 6)
#imagelabel.place(x=250, y=250, anchor="center")
#imagelabel.place(x=0, y=0,anchor="center")

##backgroundImageRight = tkinter.PhotoImage(os.path.join(path_aFrame,'01.png'))
##backgroundImageRightPIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_aFrame,'01.png'))
##imagelabelright = tkinter.Label(rightrightframe,image = backgroundImageRightPIL)
##imagelabelright.place(x=0, y=0, relwidth=1, relheight=1,anchor="nw")
##imagelabelright.image = backgroundImageRightPIL

senderlistboxframe = tkinter.Frame(root,width=330,height = 400,relief=tkinter.SUNKEN,background='yellow')
senderlistboxframe.place(x=480, y=60
                         #, relwidth=1, relheight=1
                         ,anchor="nw"
                         )
#senderlistboxframe = Frame(rightframe, relief=SUNKEN,style="BW.TLabel")
####################################################################
#senderlistboxframe.geometry('200x200')
#highlightbackground='black'
senderscrollbar = tkinter.Scrollbar(senderlistboxframe,troughcolor='black', background='saddle brown',activebackground='sandy brown')
senderscrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
#https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
#http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/listbox.html
sender_listbox = tkinter.Listbox(senderlistboxframe
                        ,relief=tkinter.FLAT
                        #,relief=tkinter.RAISED
                        #,relief=tkinter.SUNKEN
                        #,relief=tkinter.GROOVE
                        #,relief=tkinter.RIDGE       
                        ,selectmode=tkinter.SINGLE
                        ,background='black'
                        ,borderwidth=0
                        ,foreground='saddle brown'
                        ,selectforeground='orange'
                        ,selectbackground='black'
                        ,highlightcolor='saddle brown'
                        ,highlightbackground='black' #'sandy brown'
                        ,highlightthickness=0
                        ,disabledforeground='red'
                        ,activestyle=tkinter.DOTBOX
                        ,exportselection=False
                        ,yscrollcommand=senderscrollbar.set
                        ,font=global_font
                        ,height=7
                        ,width=12
                        )

#sender_listbox.place(x=0,y=0)
#sender_listbox.pack(side=LEFT, fill=Y)
#sender_listbox.grid()
sender_listbox.pack(side=tkinter.LEFT
                    #,fill=tkinter.Y
                    , expand=tkinter.YES
                    )
#sender_listbox.pack(side=LEFT)
#sender_listbox.pack(pady=20)
senderscrollbar.config(command=sender_listbox.yview)

#senderlistboxframe.pack()
#senderlistboxframe.pack(side=tkinter.LEFT,fill="both",expand=tkinter.YES)

#rightbottomframe = Frame(root,width=sizex/3*2,height = sizey/8*7,borderwidth=0,highlightthickness=0, relief=SUNKEN,style="BW.TLabel")
#rightbottomframe = tkinter.Frame(rightframe,width=sizex/3,height = sizey/8,borderwidth=0,highlightthickness=0, relief=tkinter.SUNKEN,background='black')
#rightbottomframe.grid(row=8, column=0, sticky = "sew")
#bottomT = tkinter.Text(rightbottomframe, background='black',foreground='orange',exportselection=0,height=1,padx=5,pady=5)
#bottomT.insert(tkinter.END, "entwickelt und gebaut von Jan Kästner 2018")
#bottomT.grid(row=8, column=0, sticky = "sew")

##def mouse_wheel(self, event):
##    """respond to Linux or Windows wheel event"""
##    print ('Mousewheel event.num %s, event.delta %s' % (event.num, event.delta))
##    if event.num == 5 or event.delta == -120:
##        self.max_iterations -= 120
##    if event.num == 4 or event.delta == 120:
##        self.max_iterations += 120
##    self.label['text'] = self.max_iterations
##self.bind("<MouseWheel>", self.mouse_wheel)

#downframepicture1 = PIL.ImageTk.PhotoImage(file=os.path.join(path_script + '//aNixie','zm1080_l2_09bdm_30x50_8b [www.imagesplitter.net]-0-0.gif'))
#root.downframepicture1 = downframepicture1
#downframeLabel1 = Label(master=rightbottomframe, image=downframepicture1)

#downframeCanvas1 = Canvas(rightframe)
#downframeCanvas1.create_image((0,0),image=downframepicture,anchor='nw')
####################################################################
def info(title):
    print (title)
    print ('module name:', __name__)
    print ('parent process:', os.getppid())
    print ('process id:', os.getpid())
####################################################################
def ping_requests(ip, prot='http'):
    retvalue = 0
    response = 0
    time_response = 0
    time_diff1 = 0
    time_diff2 = 0
    time_diff3 = 0
    time_diff4 = 0

    # try:
    ##    clock = time.process_time #or
    #     clock = time.perf_counter
    # except AttributeError:
    #     clock = time.clock

    try:
        #print('ping_requests: %s' % (str(prot + '://' + ip)))
        start_time1 = timeit.default_timer()
        #start_time2 = time.process_time()
        start_time2 = time.perf_counter()
        start_time3 = time.time()
        start_time4 = datetime.datetime.now()
        #http://docs.python-requests.org/en/master/user/advanced/#advanced
        #response = requests.get('http://swr-swr1-bw.cast.addradio.de')
        response = requests.get(prot + '://' + ip, timeout=0.2)
        time_response = response.elapsed
        time_diff1 = timeit.default_timer() - start_time1
        #time_diff2 = time.process_time() - start_time2
        time_diff2 = time.perf_counter() - start_time2
        time_diff3 = time.time() - start_time3
        time_diff4 = datetime.datetime.now() - start_time4
        #print('ping_requests response: %s' % (str(response)))
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        traceback.print_exc()
        print('ping_requests exceptions.HTTPError for: %s' % (err.response.text))
        time_diff1 = 0
        #raise SystemExit(err)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print('ping_requests exceptions.Timeout from: %s' % (prot + '://' + ip))
        time_diff1 = 0
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print('ping_requests exceptions.TooManyRedirects from: %s' % (prot + '://' + ip))
        time_diff1 = 0
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        #raise SystemExit(e)
    #except:
        traceback.print_exc()
        print('ping_requests exceptions.RequestException from: %s' % (prot + '://' + ip))
        time_diff1 = 0
        time_diff2 = 0
        time_diff3 = 0
        time_diff4 = 0

    if time_diff1 == 0:
        retvalue = 0
    else:
        if int(round(time_diff1 * 1000)) < int(round(time_response.microseconds / 1000)):
            print ("time ping_requests  time_response : %s" % str(int(round(time_response.microseconds / 1000))))
            print ("time ping_requests  time_diff1 : %s" % str(int(round(time_diff1 * 1000))))
            print ("time ping_requests  time_diff2 : %s" % str(int(round(time_diff2 * 1000))))
            print ("time ping_requests  time_diff3 : %s" % str(int(round(time_diff3 * 1000))))
            print ("time ping_requests  time_diff4 : %s" % str(int(round(time_diff4.microseconds / 1000))))
            retvalue = 0
        else:
            retvalue = int(round(time_response.microseconds / 1000))
    return retvalue
###########################
# https://stackoverflow.com/questions/15616378/python-network-bandwidth-monitor
def ping_gateway_task(root, trafic_stat_old,datetime_old):
    ip_sender = dicsendershost.get(sender_listbox.get(sender_listbox.curselection()))
    time_sender = ping_requests(ip_sender)
    #time_sender = ping_socket(ip_sender)
    time_sender_show = time_sender
    trafic_stat_show = 0
    datetime_diff = datetime.datetime.now()
    trafic_stat_now = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    if datetime_old:
        datetime_diff = datetime.datetime.now() - datetime_old
    datetime_old = datetime.datetime.now()
    if trafic_stat_old:
        trafic_stat_show = ((((trafic_stat_now - trafic_stat_old)*8)/3)/1000)/1000 #datetime_diff.
    trafic_stat_old = trafic_stat_now
    print ("bytes send and recieved  trafic_stat_now : %s" % str(datetime_diff)) #19953688
    print ("bytes send and recieved  trafic_stat_now : %s" % str(int(round(trafic_stat_show)))) #847443838 
    #cat /sys/class/net/<ethX>/statistics
    #cat /sys/class/thermal/thermal_zone0/temp
    #cat /sys/class/net/wlan0/wireless/link
    #cat /sys/class/net/wlan0/operstate
    #cat /sys/class/net/wlan0/carrier
    #cat /sys/class/net/eth0/statistics/rx_packets: number of packets received 
    #cat /sys/class/net/eth0/statistics/tx_packets: number of packets transmitted 
    #cat /sys/class/net/eth0/statistics/rx_bytes: number of bytes received 
    #cat /sys/class/net/eth0/statistics/tx_bytes: number of bytes transmitted 
    #cat /sys/class/net/eth0/statistics/rx_dropped: number of packets dropped while received 
    #cat /sys/class/net/eth0/statistics/tx_dropped: number of packets dropped while transmitted
    #cat /proc/cpuinfo: verwendete CPU
    #cat /proc/cpuinfo | grep processor | wc -l: Anzahl der Prozessorkerne
    #lscpu
    #vcgencmd measure_temp
    #cat /sys/class/thermal/thermal_zone0/temp
    #dmesg | grep -i bcm2835-cpufreq
    #vcgencmd measure_volts
    #vcgencmd measure_clock arm
    #ps -eo pcpu,pid -o comm= | sort -k1 -n -r | head -1 | awk '{ print $1 }'  :cpuload des belastendsten proc
    #ps -eo pcpu | awk '{cpu_load+=$1} END {print cpu_load}'        :cpuload aller procs

    if time_sender>150:
        time_sender_show=150
    elif time_sender<=0:
        time_sender_show=150

    if trafic_stat_show>150:
        trafic_stat_show=150
    elif trafic_stat_show<=0:
        trafic_stat_show=150    



    if meter1==1:
        meter1_metermg.set(int(psutil.cpu_percent(interval=None, percpu=False)))
    elif meter1==2:
        meter1_meter360.set(int(psutil.cpu_percent(interval=None, percpu=False)))
    elif meter1==3:
        meter1_meterva.set(int(psutil.cpu_percent(interval=None, percpu=False)))

    if meter2==1:
        meter2_metermg.set(int(time_sender_show))
        #meter2_metermg.set(int(trafic_stat_show))
    elif meter2==2:
        meter2_meter360.set(int(time_sender_show))
        #meter2_meter360.set(int(trafic_stat_show))
    elif meter2==3:
        meter2_meterva.set(int(time_sender_show))
        #meter2_meterva.set(int(trafic_stat_show))
    root.after(3000, ping_gateway_task, root,trafic_stat_old,datetime_old)
    #tempCPU=int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    ##        meter2_meter360.setrange(0,100000)
    ##        meter2_meter360.set(int(get_bandwidh(interface='wlan0',direction='rx')))
root.after(3000, ping_gateway_task, root,0,0)
####################################################################
def onselect(evt):
    #info('onselect')
    # Note here that Tkinter passes an event object to onselect()
    ##sender_listbox.focus()
    print ('  ---------------listbox event')
    print ('  sender_key               : "%s"' % (sender_key.get('last')))
    print ('  listbox.get(ACTIVE)      : "%s"' % (str(sender_listbox.get(tkinter.ACTIVE))))
    print ('  listbox.get(ANCHOR)      : "%s"' % (str(sender_listbox.get(tkinter.ANCHOR))))
    #print ('  listbox.curselection()[0]: "%s"' % (str(sender_listbox.curselection()[0])))
    w = evt.widget
    index = int(w.curselection()[0])
    list_value = w.get(index)
    if not(str(w.get(tkinter.ANCHOR)) == str(w.get(tkinter.ACTIVE))):
        w.see(index) #sender_listbox.see(index) #todo: remove here and make it permanent visible without selection needed
        #print ('  ------------------------------------------------------------- changed')
        print ('You selected new item %d: "%s"' % (index, list_value))
        #print ('  ---------------index')
        #print ('  sender_key               : "%s"' % (sender_key.get('last')))
        #print ('  w.get(ACTIVE)      : "%s"' % (str(w.get(tkinter.ACTIVE))))
        #print ('  w.get(ANCHOR)      : "%s"' % (str(w.get(tkinter.ANCHOR))))
        #print ('  w.curselection()[0]: "%s"' % (str(w.curselection()[0])))
        #w.selection_anchor(index)    #normally not needed, because allready correct
        #w.activate(index) #todo: activate it at the end of onselect
        #w.itemconfig(1, {'bg':'red'})
        #w.itemconfig(tkinter.ACTIVE,{'bg':'red'})
        #w.itemconfig(index, foreground='yellow')
        if not str(sender_key.get('last')) == list_value:   #str(w.get(tkinter.ANCHOR)):
            set_last_sender_to_file( path_file_sender, list_value,'1' )
        process_stop_radio()
        #dicsendersping[list_value] = do_ping(dicsendershost.get(list_value))
        process_start_radio(dicsenders.get(list_value))
        w.activate(index) #todo: activate it at the end of onselect
        w.selection_anchor(index)    #normally not needed, because allready correct
    else:
        print ('You reselected item %d: "%s" and state should be: %s' % (index, list_value, str(sender_key.get('state'))))
        if (str(sender_key.get('state')) == '1'):
            print ('  ---------------state running - we stop now')
            process_stop_radio()
            set_last_sender_to_file( path_file_sender, list_value,'0' )
        else:
            print ('  ---------------state stoped - we start now')
            process_stop_radio()
            process_start_radio(dicsenders.get(list_value))
            set_last_sender_to_file( path_file_sender, list_value,'1' )

    t3b.delete('1.0', tkinter.END)
    t3b.insert(tkinter.END, "JK Radio (2018) V:%s" % str(version),'JK')
    #t3b.delete("end-1c linestart", tkinter.END)
    t3b.insert(tkinter.END, '\n' + dicsendershost.get(list_value), 'STATE')
    #t3b.insert("%d.%d" % (2, 0), '\n' + dicsendershost.get(list_value), 'STATE')
    if str(sender_key.get('state')) == '1':
        t3b.tag_config('STATE', foreground='green')
    elif str(sender_key.get('state')) == '0':
        t3b.tag_config('STATE', foreground='red')
    else:
        t3b.tag_config('STATE', foreground='yellow')
    time.sleep(1)
    if not sys.platform == "win32":
        if process_exists('omxplayer') or process_exists('mplayer'):
            #button3apressed.set(1)
            button3a.configure(image=charging_trueImagePIL)
        else:
            #button3apressed.set(0)
            button3a.configure(image=charging_falseImagePIL)
    else:
        if process_exists('wmplayer'):
            #button3apressed.set(1)
            button3a.configure(image=charging_trueImagePIL)
        else:
            #button3apressed.set(0)
            button3a.configure(image=charging_falseImagePIL)

def volumeUp():
    print ("Button volumeUp")
    #subprocess.call("volup", shell=True)
def volumeDown():
    print ("Button volumeDown")
    #subprocess.call("voldown", shell=True)
def channelDown(channel):
    print ("Button channelDown from: %d %s" % (int(sender_listbox.curselection()[0]),str(sender_listbox.get(int(sender_listbox.curselection()[0])))))
    selection_indices = sender_listbox.curselection()
    # default next selection is the beginning
    next_selection = 0
    # make sure at least one item is selected
    if len(selection_indices) > 0:
        # Get the last selection, remember they are strings for some reason so convert to int
        last_selection = int(selection_indices[-1])
        print ("Button channelDown last_selection: %d size %s" % (last_selection,str(sender_listbox.size())))
        # clear current selections
        sender_listbox.selection_clear(selection_indices)
        # Make sure we're not at the last item
        if last_selection < sender_listbox.size() - 1:
            next_selection = last_selection + 1
        sender_listbox.activate(next_selection)
        sender_listbox.selection_set(next_selection)
        sender_listbox.event_generate("<<ListboxSelect>>")
def channelUp(channel):
    print ("Button channelUp from: %d %s" % (int(sender_listbox.curselection()[0]),str(sender_listbox.get(int(sender_listbox.curselection()[0])))))
    selection_indices = sender_listbox.curselection()
    # default next selection is the end
    next_selection = sender_listbox.size()-1
    # make sure at least one item is selected
    if len(selection_indices) > 0:
        # Get the last selection, remember they are strings for some reason so convert to int
        last_selection = int(selection_indices[-1])
        print ("Button channelUp last_selection: %d size %s" % (last_selection,str(sender_listbox.size())))
        # clear current selections
        sender_listbox.selection_clear(selection_indices)
        # Make sure we're not at the last item
        if last_selection > 0:
            next_selection = last_selection - 1
        sender_listbox.activate(next_selection)
        sender_listbox.selection_set(next_selection)
        sender_listbox.event_generate("<<ListboxSelect>>")
####################################################################
dicsenders = {}
dicsendershost = {}
dicsendersip = {}
dicsendersping = {}
with open(path_file_senders,"r") as atemp_file:
    for aline in atemp_file:
        if not aline.startswith('#') and not aline.startswith('version') and aline.strip():
            (akey, avalue) = aline.split("|")
            print ("akey: %s  avalue: %s" % (akey,avalue))
            dicsenders[akey] = avalue.strip('\n')
            temp_host = urllib.parse.urlsplit(avalue)
            temp_ip = socket.gethostbyname(temp_host.hostname)
            dicsendershost[akey] = temp_host.hostname
            dicsendersip[akey] = temp_ip
            dicsendersping[akey] = 0
sender_key = {}
def set_last_sender_to_file(path_file_sender,sender,state):
    sender_key['last'] = str(sender)
    sender_key['state'] = str(state) 
    #print ("file open to write: %s" % path_file_sender)
    with open(path_file_sender,"w") as ctemp_file:
        ctemp_file.write("last|" + str(sender) + '\n')
        ctemp_file.write("state|" + str(state) + '\n')
        return 0
#sender_key['state'] = str(state) 
#str(sender_key.get('last'))
#sender_key['last'] = 'swr3'
#sender_key['state'] = '0'
if os.path.isfile(path_file_sender):
    with open(path_file_sender,"r") as btemp_file:
        for bline in btemp_file:
            if bline.startswith('last|'):
                print ("bline: %s" % bline)
                (bkey, bvalue) = bline.split("|")
                if bvalue.strip('\n') in dicsenders.keys():
                    sender_key['last'] = bvalue.strip('\n')
                    print ("sender from file: %s" % str(sender_key.get('last')))
            elif bline.startswith('state|'):
                (bkey, bvalue) = bline.split("|")
                sender_key['state'] = bvalue.strip('\n')
                print ("state from file: %s" % str(sender_key.get('state')))
else:
    set_last_sender_to_file(path_file_sender,'swr3','0')


####################################################################
##print ("-----------------------------------------------------------")
##for dkey in dicsenders.keys():
##    print ("dkey: %s  dicsenders: %s  dicsenders: %s  dicsenders: %s  dicsenders: %s" % (dkey, dicsenders.get(dkey),dicsendershost.get(dkey),dicsendersip.get(dkey),dicsendersping.get(dkey) ))
##print ("-----------------------------------------------------------")
##for ekey in sender_key.keys():
##    print ("ekey: %s  sender_key: %s" % (ekey, sender_key.get(ekey) ))
##print ("-----------------------------------------------------------")
####################################################################
sender_listbox.config(yscrollcommand=senderscrollbar.set, selectmode = tkinter.SINGLE, exportselection=False )
#sender_listbox.config(yscrollcommand=senderscrollbar.set)
senderscrollbar.config(command=sender_listbox.yview)
#####################################
sender_listbox.delete(0, tkinter.END)
#for fkey, fvalue in dicsenders:
#for fkey in dicsenders:
for fkey in  sorted(dicsenders.keys()):
    print (' sender_listbox item key: %s' % str(fkey))
    sender_listbox.insert(tkinter.END, str(fkey))
    #sender_listbox.tag_config(item, foreground='red')
    #sender_listbox.insert('insert', ' red text', 'RED')
    #sender_listbox.tag_config('RED', foreground='red')
#len_max = 0
#list_items = ["item2", "item2", "item3+a few characters for the size"]
#for m in list_items:
#    if len(m) > len_max:
#        len_max = len(m)
#for i in range(20):
#    sender_listbox.insert(END, i)
#####################################
#The selection_set method adds an item to the current selection. This may or may not unselect other items, depending on your selection mode.
#If you want to guarantee that you always get just that one item selected no matter what, you can clear the selection with selection_clear(0, END), then selection_set that one item.
#If you want to also make the selected item active, also call activate on the item after setting it.
sender_listbox.selection_clear(0, tkinter.END)
print ('  last_sender: "%s"' % (str(sender_key.get('last'))))
last_sender_key_as_index = int(list(dicsenders.keys()).index(str(sender_key.get('last'))))
print ('  last_sender_as_index: "%d"' % last_sender_key_as_index)
print ('  last_sender_from_list: "%s"' % str(sender_listbox.get(last_sender_key_as_index)))
sender_listbox.see(last_sender_key_as_index)
sender_listbox.activate(last_sender_key_as_index)
sender_listbox.selection_set(last_sender_key_as_index)
sender_listbox.selection_anchor(last_sender_key_as_index)
#print ('  listbox.get(ACTIVE): "%s"' % (str(sender_listbox.get(tkinter.ACTIVE))))
#print ('  size (line count): "%s"' % (sender_listbox.size()))

#sender_listbox.bind( '<Double-1>', ( lambda event: onDoubleClick() ) ) # a lambda-wrapped CallBackHANDLER()
# onDoubleClick: get messages selected in listbox 
sender_listbox.bind('<<ListboxSelect>>', onselect)
sender_listbox.focus()
sender_listbox.event_generate("<<ListboxSelect>>")
####################################################################

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag #pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffersize=4096)
try:
    pygame.mixer.init()
    sound_exist=1
except:
    traceback.print_exc()
    sound_exist=0
if sound_exist==1:
    #pygame.mixer.music.load(os.path.join(path_aNixie,'relay.wav'))
    #root.after(0, pygame.mixer.music.play(loops=10, start=0.0))
    #print (pygame.mixer.music.get_volume())
    #root.after(500, pygame.mixer.music.play(loops=10, start=0.0))
    #while pygame.mixer.get_busy() == True:
    #while pygame.mixer.music.get_busy() == True:
    #    continue

    ##sound = pygame.mixer.Sound("s.wav")
    ##channel = s.play()      # Sound plays at full volume by default
    ##sound.set_volume(0.9)   # Now plays at 90% of full volume.
    ##sound.set_volume(0.6)   # Now plays at 60% (previous value replaced).
    ##channel.set_volume(0.5)
    effect_on = pygame.mixer.Sound(os.path.join(path_aSound,'on1.wav'))
    effect_on.set_volume(1)
    ##effect_on.play()
    ##while pygame.mixer.get_busy() == True:
    ###while pygame.mixer.music.get_busy() == True:
    ##    continue

    effect_relay = pygame.mixer.Sound(os.path.join(path_aSound,'relay.wav'))
    effect_relay.set_volume(1)
    print (effect_relay.get_length())
    jitter=effect_relay.get_length() * 1000
    print (jitter)
    jitter=round(jitter /6)
    print (jitter)
    #root.after(0, effect_shutdown.play)
    #effect_shutdown.play()
    effect_relay.play(loops=10)
    root.after(jitter, effect_relay.play,3)
    root.after(2*jitter, effect_relay.play,1)
    root.after(3*jitter, effect_relay.play,2)
    root.after(4*jitter, effect_relay.play,3)
    root.after(5*jitter, effect_relay.play,8)
    root.after(6*jitter, effect_relay.play,5)

    #root.after(jitter, effect_relay.play)

    effect_shutdown = pygame.mixer.Sound(os.path.join(path_aSound,'shutdown1.wav'))
    effect_shutdown.set_volume(1)

def readVolume():
    value = os.popen("amixer get PCM|grep -o [0-9]*%|sed 's/%//'").read()
    return int(value)
def rotaryChange(direction):
    volume_step = 5
    volume = readVolume()
    if direction == 1:
        os.system("sudo amixer set PCM -- "+str(min(100,max(0,volume + volume_step)))+"%")
    else:
        os.system("sudo amixer set PCM -- "+str(min(100,max(0,volume - volume_step)))+"%")

def powerOff(ButtonOff=4):
    subprocess.call(['poweroff'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


CLOCKWISE=1
ANTICLOCKWISE=2
BUTTONDOWN=3
BUTTONUP=4
rotary_a = 0
rotary_b = 0
rotary_c = 0
last_state = 0
direction = 0
Rotary_counter=0  # starting point for the running directional counter

def switch_event(switch):
    if GPIO.input(clk):
        rotary_a = 1
    else:
        rotary_a = 0
    if GPIO.input(dt):
        rotary_b = 1
    else:
        rotary_b = 0
    global Rotary_counter, last_state, direction
    rotary_c = rotary_a ^ rotary_b
    new_state = 0
    new_state = rotary_a * 4 + rotary_b * 2 + rotary_c * 1
    delta = (new_state - last_state) % 4
    last_state = new_state
    event = 0
    if delta == 1:
        if direction == CLOCKWISE:
            Rotary_counter += 1
            print ("Clockwise -> %s" % str(Rotary_counter))
            event = direction
        else:
            direction = CLOCKWISE
    elif delta == 3:
        if direction == ANTICLOCKWISE:
            Rotary_counter -= 1
            print ("Anticlockwise <- %s" % str(Rotary_counter))
            event = direction
        else:
            direction = ANTICLOCKWISE
##    if event > 0:
##        callback(event)
##    return

Rotary_counter = 0              # Start counting from 0
Current_A = 1                   # Assume that rotary switch is not
Current_B = 1                   # moving while we init software
LockRotary = threading.Lock()
def rotary_interrupt(A_or_B):
    global Rotary_counter, Current_A, Current_B, LockRotary
    Switch_A = GPIO.input(clk)
    Switch_B = GPIO.input(dt)
    # now check if state of A or B has changed # if not that means that bouncing caused it
    if Current_A == Switch_A and Current_B == Switch_B: # Same interrupt as before (Bouncing)?
        return                                          # ignore interrupt!
    Current_A = Switch_A                                # remember new state
    Current_B = Switch_B                                # for next bouncing check
    if (Switch_A and Switch_B):                     # Both one active? Yes -> end of sequence
        LockRotary.acquire()                        # get lock
        if A_or_B == dt:                         # Turning direction depends on
            Rotary_counter += 1                     # which input gave last interrupt
            print ("Clockwise -> %s" % str(Rotary_counter))
            channelDown(Rotary_counter)
        else:                                       # so depending on direction either
            Rotary_counter -= 1                     # increase or decrease counter
            print ("Anticlockwise <- %s" % str(Rotary_counter))
            channelUp(Rotary_counter)
        LockRotary.release()                        # and release lock
    return
    
if gpio_exist == 1:
    #CLK - GPIO23 (pin16)         GPIO17 (pin 11)
    #DT  - GPIO24 (pin18)         GPIO18 (pin 12)
    #+   - 3v3 (pin1)
    #GND - GND (pin6)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    #https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=133740
    clk = 27  # Encoder input A: input GPIO23 (active high) pin 16
    dt = 17  # Encoder input B: input GPIO24 (active high) pin 18  pull_up_down=GPIO.PUD_DOWN
    if 0==1:
        GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # setup an event detection thread for the A encoder switch   RISING ,FALLING bouncetime=5 bouncetime in mSec
        GPIO.add_event_detect(clk, GPIO.FALLING, callback=switch_event)
        GPIO.add_event_detect(dt, GPIO.FALLING, callback=switch_event)
    else:
        GPIO.setup(clk, GPIO.IN)
        GPIO.setup(dt, GPIO.IN)
        # setup an event detection thread for the A encoder switch   RISING ,FALLING bouncetime=5 bouncetime in mSec
        GPIO.add_event_detect(clk, GPIO.RISING, callback=rotary_interrupt) 
        GPIO.add_event_detect(dt, GPIO.RISING, callback=rotary_interrupt)
    #root.after(1000, readEncoder)

    ButtonAnAus = 22 # GPIO-18 pin 12
    GPIO.setup(ButtonAnAus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ButtonAnAus, GPIO.FALLING, callback=button3aclick, bouncetime=500)
    
    ButtonOff = 18 # GPIO-4 pin 7
    GPIO.setup(ButtonOff, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ButtonOff, GPIO.FALLING, callback=powerOff, bouncetime=5)

process_stop_radio()
root.focus_set()
root.mainloop()
exitfunc()
#root.destroy()
