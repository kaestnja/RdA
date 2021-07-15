#!/usr/bin/python3
version=184

#      nano /home/pi/.config/lxsession/LXDE-pi/autostart # and enter the following lines or:
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart # and enter the following lines:

# sudo nano /etc/xdg/lxsession/LXDE-pi/sshpwd.sh # and enter the following line as second line:
#return ${retVal} 2>/dev/null || exit ${retVal}

# pip3 install --upgrade versioneer https://github.com/warner/python-versioneer
# pip3 install --upgrade versioneer2

# python -m pip install --upgrade pygame
# python -m pip install --upgrade requests
# python -m pip install git+https://github.com/sn4k3/FakeRPi

# sudo apt-get install pop-theme
# sudo apt-get install -y fontconfig-config

## sudo apt install unclutter
# 


modulname = 'anneradio'
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
from urllib import parse  # ,request

import PIL      #sudo apt-get install python3-pil.imagetk  or  pip3 install pillow  or  python -m pip install pillow
import psutil   #sudo apt-get install python3-psutil
#import resource
#subprocess.Popen(['omxplayer','-b',os.path.join(path_aNixie,'shutdown.wav')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
#https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.get_length
import pygame
#import re
##################################
import requests
from PIL import ImageTk  # ,Image

#import urllib.parse
#from urllib.parse import urlsplit, urlunsplit
##################################
import jksip as jksip
import jksmeter360 as meter360
import jksmetermg as metermg
#from theRadio import jksmeterva as meterva
import jksmeterva as meterva
import jksnixieclock as nixieclock

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
    #os.environ.__setitem__('DISPLAY', ':0.0')
    os.environ['DISPLAY']=':0.0'

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
##################################
sender_key = {}
sender_key['last'] = 'swr3'
sender_key['state'] = 'True'
sender_key['sound'] = 'True'
path_aGauge = os.path.join(sys.path[0],'aGauge')
path_aNixie = os.path.join(sys.path[0],'aNixie')
path_bImages = os.path.join(sys.path[0],'bImages')
path_aFrame = os.path.join(sys.path[0],'aFrame')
path_aSound = os.path.join(sys.path[0],'aSound')
path_aMagicEye = os.path.join(sys.path[0],'aMagicEye')
path_file_senders = os.path.join(sys.path[0], 'senderlist.txt')
path_file_sender = os.path.join(sys.path[0], 'sender.txt')
try:
    import pygame #    sudo pip3 install --upgrade pygame
    import pygame.mixer
    # import time
    # from array import array
    # from pygame.locals import *
    pygame.init()
    # pygame.__init__()
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag #pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffersize=4096)
    #pygame.mixer.__init__()
    # pygame.mixer.Sound.init(self, buffer=self.build_samples())
    # pygame.mixer.init()
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(path_aSound,'on1.wav'))
    #effect_on = pygame.mixer.Sound(os.path.join(path_aSound,'on1.wav'))
except:
    sender_key['sound'] = 'False'
###########################################################################
# https://bugs.python.org/issue28165 The 'subprocess' module leaks memory when called in certain ways
def process_exists(proc_name):
    #cmd = 'pgrep -x "omxplayer" > /dev/null 2>&1'
    cmd1 = 'pgrep -x "'
    cmd2 = '" > /dev/null 2>&1'
    cmd = cmd1 + proc_name + cmd2
    retvalue = True
    try:
        p1 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
        #p1 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p1output = p1.communicate()[0]
        if (p1.returncode == 1 ):
            retvalue = False
        #print(stime + " loop: " + str(count) + " p1return:" + str(p1.returncode))
        p1.kill()
    except:
        retvalue = True
    return retvalue
def process_do(cmd):
    retvalue = True
    try:
        p2 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
        #p2 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p2output = p2.communicate()[0]
        if (p2.returncode == 1 ):
            retvalue = False
        p2.kill()
    except:
        retvalue = True
    return retvalue
###########################################################################
root = tkinter.Tk()
#os.system('pkill omxplayer')
process_do('sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1')
process_do('sudo pkill -SIGKILL -f "omxplayer.bin" > /dev/null 2>&1')
root.overrideredirect(1)
root.wm_attributes("-topmost", True)
########################################################################################
charging_trueImage = tkinter.PhotoImage(os.path.join(path_bImages,'button_true_105x42.png'))
charging_trueImagePIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_bImages,'button_true_105x42.png'))
charging_falseImage = tkinter.PhotoImage(os.path.join(path_bImages,'button_false_105x42.png'))
charging_falseImagePIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_bImages,'button_false_105x42.png'))
####################################################################
dicsenders = {}
dicsendershost = {}
dicsendersip = {}
dicsendersping = {}
with open(path_file_senders,"r") as atemp_file:
    for aline in atemp_file:
        if not aline.startswith('#') and not aline.startswith('version') and aline.strip():
            (akey, avalue) = aline.split("|")
            dicsenders[akey] = avalue.strip('\n')
            #print ("%s | %s" % (akey,dicsenders[akey]))
            temp_host = urllib.parse.urlsplit(avalue)
            try:
                temp_ip = socket.gethostbyname(temp_host.hostname)
            except:
                temp_ip = temp_host.hostname
            dicsendershost[akey] = temp_host.hostname
            dicsendersip[akey] = temp_ip
            dicsendersping[akey] = 0
            #print ("   %s  | %s" % (dicsendershost[akey],dicsendersip[akey]))
if os.path.isfile(path_file_sender):
    with open(path_file_sender,"r") as btemp_file:
        for bline in btemp_file:
            if bline.startswith('last|'):
                #print ("bline: %s" % bline)
                (bkey, bvalue) = bline.split("|")
                if bvalue.strip('\n') in dicsenders.keys():
                    sender_key['last'] = bvalue.strip('\n')

#def button1aclick():
#    button1a.configure(image=charging_falseImagePIL)
#    exitfunc()
#def button1bclick():
#    button1b.configure(image=charging_falseImagePIL)
#def button3aclick(ButtonAnAus=18):
#    os.system('pkill omxplayer')
#    if (str(sender_key.get('state')) == '1'):
#        set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'0' )
#    else:
#        radio_station=dicsenders.get(str(sender_key.get('last')))
#        subprocess.Popen(['omxplayer', '-o','local', radio_station,'&'])
#        set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'1' )
#    t3b.delete('1.0', tkinter.END)
#    t3b.insert(tkinter.END, "JK Radio (2018) V:%s" % str(version),'JK')
#    t3b.insert(tkinter.END, '\n' + dicsendershost.get(str(sender_key.get('last'))), 'STATE')

##########################
def exitfunc():
    #print ("file open to write: %s" % path_file_sender)
    if (process_exists('omxplayer') == True):
        #os.system('pkill omxplayer')
        #subprocess.call('sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1', shell=True)
        process_do('sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1')
        process_do('sudo pkill -SIGKILL -f "omxplayer.bin" > /dev/null 2>&1')
    if sender_key.get('sound'):
        effect_shutdown.play()
        #while pygame.mixer.music.get_busy() == True:
        while pygame.mixer.get_busy():
            continue
    GPIO.cleanup(dt)
    GPIO.cleanup(clk)
    # GPIO.cleanup(ButtonAnAus)
    root.quit()
    quit()
    # sys.exit() #exit with exception, used to exit treads
    # root.destroy()

def exit(event):
    exitfunc()

def on_closing():
    exitfunc()
    
sys.exitfunc = exitfunc
root.bind("<Escape>", exit)
########################################################################################
global global_font
appHighlightFont = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
tkinter.font.families()
helv36 = tkinter.font.Font(family="Helvetica",size=36,weight="bold")
#helv36 = ("Helvetica", 36, "bold")
nixie12 = tkinter.font.Font(family="Nixie One",size=12,weight="bold")
nixie18 = tkinter.font.Font(family="Nixie One",size=18,weight="bold")
nixie24 = tkinter.font.Font(family="Nixie One",size=24,weight="bold")
nixie36 = tkinter.font.Font(family="Nixie One",size=36,weight="bold")
global_font = nixie24

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
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
if (screen_height - taskbar_height > sizey):
    posy  = screen_height - taskbar_height - sizey
root.geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
root.configure(background='black')

clock_nixieclock = nixieclock.Clock(root,width=440,height = 220) #,borderwidth=0,highlightthickness=0)
clock_nixieclock.place(x=0, y=0)    #, relwidth=1, relheight=1 ,anchor="nw")

global meter1
##meter1 = metermg.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
##meter1 = meter360.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
meter1 = meterva.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
meter1.setrange(0,100,typetxt='cpu')
meter1.place(x=0, y=220)

global meter2
##meter2 = metermg.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
##meter2 = meter360.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
meter2 = meterva.Meter(root,width=220,height = 220,borderwidth=0,highlightthickness=0)
meter2.setrange(0,100,typetxt='C°')
meter2.place(x=220, y=220)

##############################################
btframe1 = tkinter.Frame(root,width=220,height = 40)#,borderwidth=0,highlightthickness=0,relief=tkinter.FLAT,background='green')
btframe1.place(x=0, y=440)
t1a = tkinter.Text(btframe1, background='black',foreground='orange',borderwidth=0,highlightthickness=0)
t1a.delete(1.0, tkinter.END)
t1a.insert(tkinter.END, str("t1a"))
t1a.place(x=0, y=0)
#button1apressed = tkinter.IntVar()
#button1a = tkinter.Button(t1a, text="Beenden", font=nixie12, padx=5
#                          ,height=35,relief=tkinter.RAISED,background='black',foreground='orange',borderwidth=0,highlightthickness=0
#                          ,highlightcolor='orange',highlightbackground='orange',disabledforeground='red'
#                          ,compound=tkinter.CENTER,image=charging_trueImagePIL,command=button1aclick)
#t1a.window_create(tkinter.INSERT, window=button1a)

t1b = tkinter.Text(btframe1, background='black',foreground='orange',borderwidth=0,highlightthickness=0)
t1b.delete(1.0, tkinter.END)
t1b.insert(tkinter.END, str("t1b"))
t1b.place(x=110, y=0)
#button1bpressed = tkinter.IntVar()
#button1b = tkinter.Button(t1b, text="CPU/Tmp", font=nixie12, padx=5
#                          ,height=35,relief=tkinter.RAISED,background='black',foreground='orange',borderwidth=0,highlightthickness=0
#                          ,highlightcolor='orange',highlightbackground='orange',disabledforeground='red'
#                          ,compound=tkinter.CENTER,image=charging_falseImagePIL,command=button1bclick)
#t1b.window_create(tkinter.INSERT, window=button1b)
##############################################
btframe2 = tkinter.Frame(root,width=220,height = 40,borderwidth=0,highlightthickness=0)
btframe2.place(x=220, y=440)
t2a = tkinter.Text(btframe2, background='black',foreground='orange',borderwidth=0,highlightthickness=0,relief=tkinter.SUNKEN)
t2a.delete(1.0, tkinter.END)
t2a.insert(tkinter.END, str("t2a"))
t2a.place(x=0, y=0)
##############################################
btframe3 = tkinter.Frame(root,width=360,height = 40,borderwidth=0,highlightthickness=0) #, relief=tkinter.RAISED,background='red')
btframe3.place(x=440, y=440)
t3a = tkinter.Text(btframe3, background='black',foreground='orange',borderwidth=0,highlightthickness=0,relief=tkinter.SUNKEN)
t3a.delete(1.0, tkinter.END)
t3a.insert(tkinter.END, str("t3a"))
t3a.place(x=0, y=0)
#######################################################################################################################
backgroundImageMidPIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_aFrame,'template_360x440.png'))
imagelabelmid = tkinter.Label(root,width=360,height = 440,borderwidth=0,highlightthickness=0,image = backgroundImageMidPIL)
imagelabelmid.place(x=440, y=0)
imagelabelmid.image = backgroundImageMidPIL
senderlistboxframe = tkinter.Frame(root,width=330,height = 400,relief=tkinter.SUNKEN,background='yellow')
senderlistboxframe.place(x=480, y=60,anchor="nw")
senderscrollbar = tkinter.Scrollbar(senderlistboxframe,troughcolor='black', background='saddle brown',activebackground='sandy brown')
senderscrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
sender_listbox = tkinter.Listbox(senderlistboxframe
                        #,relief=tkinter.FLAT
                        #,relief=tkinter.RAISED
                        #,relief=tkinter.SUNKEN
                        #,relief=tkinter.GROOVE
                        ,relief=tkinter.RIDGE       
                        ,selectmode=tkinter.SINGLE,background='black',borderwidth=0,foreground='saddle brown',selectforeground='orange',selectbackground='black'
                        ,highlightcolor='saddle brown',highlightbackground='sandy brown',highlightthickness=0,disabledforeground='red'
                        ,activestyle=tkinter.DOTBOX
                        ,exportselection=False,yscrollcommand=senderscrollbar.set,font=global_font,height=7,width=12)
sender_listbox.pack(side=tkinter.LEFT, expand=tkinter.YES)
senderscrollbar.config(command=sender_listbox.yview)
####################################################################
def ping_requests(ip, prot='http'):
    retvalue = 0
    response = 0
    time_response = 0
    time_diff1 = 0

    try:
        start_time1 = timeit.default_timer()
        #http://docs.python-requests.org/en/master/user/advanced/#advanced
        #response = requests.get('http://swr-swr1-bw.cast.addradio.de')
        response = requests.get(prot + '://' + ip, timeout=0.2)
        time_response = response.elapsed
        time_diff1 = timeit.default_timer() - start_time1
    except:
        traceback.print_exc()
        print('ping_requests exception from: %s' % (prot + '://' + ip))
        time_diff1 = 0
    if not(time_diff1 == 0):
        if int(round(time_diff1 * 1000)) < int(round(time_response.microseconds / 1000)):
            retvalue = 0
        else:
            retvalue = int(round(time_response.microseconds / 1000))
    response = 0
    time_response = 0
    time_diff1 = 0
    return retvalue
###########################
def ping_gateway_task(root):
    ip_sender = dicsendershost.get(str(sender_key.get('last')))
    time_sender = 0
    #time_sender = ping_requests(ip_sender)
    time_sender_show = time_sender
    t3a.delete(1.0, tkinter.END)
    t3a.insert("%d.%d" % (1, 0), "JK Radio (2018) V:%s" % str(version),'JK')
    t3a.tag_config('address', foreground='yellow')
    t3a.insert("%d.%d" % (2, 0), "\n%s" % ip_sender, 'address')
    if ((time_sender > 150) or (time_sender <= 0)):
        time_sender_show=150
        t3a.tag_config('address', foreground='red')
    else:
        t3a.tag_config('address', foreground='green')
    lastCPU = 0,14
    try:
        lastCPU = int(psutil.cpu_percent(interval=None, percpu=False))
    except:
        breakpoint
    tempCPU = 14
    try:
        tempCPU = round(int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3)
    except:
        breakpoint
    t1a.delete(1.0, tkinter.END)
    t1a.insert("%d.%d" % (1, 0), "CPU Last: %s" % str(lastCPU),'cpulast')
    t1a.tag_config('cpulast', foreground='green')
    t1a.insert("%d.%d" % (2, 0), "\nCPU Temp: %s" % str(tempCPU), 'cputemp')
    t1a.tag_config('cputemp', foreground='orange')
   
    meter1.set(lastCPU)

    #meter2.set(int(time_sender_show))
    meter2.set(tempCPU)
    
    t1b.delete(1.0, tkinter.END)
    try:
        t1b.insert("%d.%d" % (1, 0), "GPIO: %s" % str(bool( GPIO.input(ButtonAnAus))),'gpio')
        t1b.tag_config('gpio', foreground='green')
    except:
        t1b.insert("%d.%d" % (1, 0), "GPIO: %s" % str("chrashed"),'gpio')
        t1b.tag_config('gpio', foreground='red')
    try:
        t1b.insert("%d.%d" % (2, 0), "\nstate: %s" % str(sender_key.get('state')), 'state')
        t1b.tag_config('state', foreground='orange')
    except:
        t1b.insert("%d.%d" % (2, 0), "\nstate: %s" % str("chrashed"), 'state')
        t1b.tag_config('state', foreground='red')
    
    
    #https://chase-seibert.github.io/blog/2013/08/03/diagnosing-memory-leaks-python.html
    #https://benbernardblog.com/tracking-down-a-freaky-python-memory-leak/
    t2a.delete(1.0, tkinter.END)
    t2a.insert("%d.%d" % (1, 0), "Play: %s" % str('omxplayer'),'player')
    t2a.tag_config('player', foreground='green')
    proc_exists = 'False'
    if process_exists('omxplayer'):proc_exists = 'True'
    t2a.insert("%d.%d" % (2, 0), "\nproc: %s" % proc_exists, 'process')
    t2a.tag_config('process', foreground='orange')
    
    root.after(5000, ping_gateway_task, root)
    ##        meter2_meter360.setrange(0,100000)
    ##        meter2_meter360.set(int(get_bandwidh(interface='wlan0',direction='rx')))
####################################################################
def ping_process_task(root):
    #sender_key['state'] = str(bool( GPIO.input(ButtonAnAus))) 
    #print ("ping_process_task, last: %s state : %s" % (str(sender_key.get('last')),str(sender_key.get('state'))))
    #if ('True' in str(sender_key.get('state'))): 
    if GPIO.input(ButtonAnAus):
        if (process_exists('omxplayer') == False):
            radio_station=dicsenders.get(str(sender_key.get('last')))
            #subprocess.Popen(['omxplayer', '-o','local', radio_station,'&'])
            subprocess.Popen(['omxplayer', '-o',sound_out_type, radio_station,'&'])
            with open(path_file_sender,"w") as ctemp_file:
                ctemp_file.write("last|" + str(sender_key.get('last')) + '\n')
    else:
        if (process_exists('omxplayer') == True):
            #os.system('pkill omxplayer')
            #subprocess.call('sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1', shell=True)
            process_do('sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1')
            process_do('sudo pkill -SIGKILL -f "omxplayer.bin" > /dev/null 2>&1')
            with open(path_file_sender,"w") as ctemp_file:
                ctemp_file.write("last|" + str(sender_key.get('last')) + '\n')
    root.after(2000, ping_process_task, root)
def process_kill(channel):
    if (sender_key.get('sound') == True):
        effect_shutdown.play()
        #while pygame.mixer.music.get_busy() == True:
        while pygame.mixer.get_busy():
            continue
    
def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    list_value = w.get(index)
    if not(str(w.get(tkinter.ANCHOR)) == str(w.get(tkinter.ACTIVE))):
        w.see(index) #sender_listbox.see(index) #todo: remove here and make it permanent visible without selection needed
        w.activate(index) #todo: activate it at the end of onselect
        w.selection_anchor(index)    #normally not needed, because allready correct
        if not str(sender_key.get('last')) == list_value:   #str(w.get(tkinter.ANCHOR)):
            sender_key['last'] = str(list_value)
            #sender_key['state'] = str(bool( GPIO.input(ButtonAnAus)))
            #print ("onselect, last: %s state : %s" % (str(sender_key.get('last')),str(sender_key.get('state'))))
            if (process_exists('omxplayer') == True):
                #os.system('pkill omxplayer')
                #subprocess.call('sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1', shell=True)
                process_do('sudo pkill -SIGKILL -f "omxplayer" > /dev/null 2>&1')
                process_do('sudo pkill -SIGKILL -f "omxplayer.bin" > /dev/null 2>&1')

def volumeUp():
    print ("Button volumeUp")
    #subprocess.call("volup", shell=True)
def volumeDown():
    print ("Button volumeDown")
    #subprocess.call("voldown", shell=True)
def channelDown(channel):
    selection_indices = sender_listbox.curselection()
    next_selection = 0
    if len(selection_indices) > 0:
        last_selection = int(selection_indices[-1])
        sender_listbox.selection_clear(selection_indices)
        if last_selection < sender_listbox.size() - 1:
            next_selection = last_selection + 1
        sender_listbox.activate(next_selection)
        sender_listbox.selection_set(next_selection)
        sender_listbox.event_generate("<<ListboxSelect>>")
def channelUp(channel):
    selection_indices = sender_listbox.curselection()
    next_selection = sender_listbox.size()-1
    if len(selection_indices) > 0:
        last_selection = int(selection_indices[-1])
        sender_listbox.selection_clear(selection_indices)
        if last_selection > 0:
            next_selection = last_selection - 1
        sender_listbox.activate(next_selection)
        sender_listbox.selection_set(next_selection)
        sender_listbox.event_generate("<<ListboxSelect>>")

####################################################################
sender_listbox.config(yscrollcommand=senderscrollbar.set, selectmode = tkinter.SINGLE, exportselection=False )
senderscrollbar.config(command=sender_listbox.yview)
sender_listbox.delete(0, tkinter.END)
for fkey in  sorted(dicsenders.keys()):
    #print (' sender_listbox item key: %s' % str(fkey))
    sender_listbox.insert(tkinter.END, str(fkey))
sender_listbox.selection_clear(0, tkinter.END)
try:
    last_sender_key_as_index = int(list(   sorted(dicsenders.keys())   ).index(str(sender_key.get('last'))))
except:
    last_sender_key_as_index = int(list(   sorted(dicsenders.keys())   ).index(str('swr3')))
sender_listbox.see(last_sender_key_as_index)
sender_listbox.activate(last_sender_key_as_index)
sender_listbox.selection_set(last_sender_key_as_index)
sender_listbox.selection_anchor(last_sender_key_as_index)
sender_listbox.bind('<<ListboxSelect>>', onselect)
sender_listbox.focus()
sender_listbox.event_generate("<<ListboxSelect>>")
####################################################################

if sender_key.get('sound'):
    effect_on = pygame.mixer.Sound(os.path.join(path_aSound,'on1.wav'))
    effect_on.set_volume(1)
    effect_relay = pygame.mixer.Sound(os.path.join(path_aSound,'relay.wav'))
    effect_relay.set_volume(1)
    #print (effect_relay.get_length())
    jitter=effect_relay.get_length() * 1000
    #print (jitter)
    jitter=round(jitter /6)
    #print (jitter)
    effect_relay.play(loops=10)
    #root.after(jitter, effect_relay.play,3)
    #root.after(2*jitter, effect_relay.play,1)
    #root.after(3*jitter, effect_relay.play,2)
    #root.after(4*jitter, effect_relay.play,3)
    #root.after(5*jitter, effect_relay.play,8)
    #root.after(6*jitter, effect_relay.play,5)
    effect_shutdown = pygame.mixer.Sound(os.path.join(path_aSound,'shutdown1.wav'))
    effect_shutdown.set_volume(1)

def readVolume():
    cmd = "amixer get PCM|grep -o [0-9]*%|sed 's/%//'"
    p3 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
    #p2 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p3output = p3.communicate()[0]
    if (p3.returncode == 1 ):
        retvalue = False
    p3.kill()
    value = os.popen("amixer get PCM|grep -o [0-9]*%|sed 's/%//'").read()
    return int(value)
def rotaryChange(direction):
    volume_step = 5
    volume = readVolume()
    if direction == 1:
        os.system("sudo amixer set PCM -- "+str(min(100,max(0,volume + volume_step)))+"%")
    else:
        os.system("sudo amixer set PCM -- "+str(min(100,max(0,volume - volume_step)))+"%")
def powerOff(ButtonOff):
    #subprocess.call(['poweroff'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #subprocess.call(['reboot'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_do('reboot > /dev/null 2>&1')

Rotary_counter = 0              # Start counting from 0, starting point for the running directional counter
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
        if A_or_B == dt:                            # Turning direction depends on
            Rotary_counter += 1                     # which input gave last interrupt
            #print ("Clockwise -> ListUp %s" % str(Rotary_counter))
            channelDown(Rotary_counter)
        else:                                       # so depending on direction either
            Rotary_counter -= 1                     # increase or decrease counter
            #print ("Anticlockwise <- ListDown %s" % str(Rotary_counter))
            channelUp(Rotary_counter)
        LockRotary.release()                        # and release lock
    return

#CLK - GPIO23 (pin16)         GPIO17 (pin 11)
#DT  - GPIO24 (pin18)         GPIO18 (pin 12)
#+   - 3v3 (pin1)
#GND - GND (pin6)
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=133740
    clk = 27  # Encoder input A: input GPIO23 (active high) pin 16
    dt = 17  # Encoder input B: input GPIO24 (active high) pin 18  pull_up_down=GPIO.PUD_DOWN
    GPIO.setup(clk, GPIO.IN)
    GPIO.setup(dt, GPIO.IN)
    # setup an event detection thread for the A encoder switch   RISING ,FALLING bouncetime=5 bouncetime in mSec
    GPIO.add_event_detect(clk, GPIO.RISING, callback=rotary_interrupt) 
    GPIO.add_event_detect(dt, GPIO.RISING, callback=rotary_interrupt)
    #root.after(1000, readEncoder)

    ButtonAnAus = 22 # GPIO-18 pin 12
    GPIO.setup(ButtonAnAus, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.add_event_detect(ButtonAnAus, GPIO.FALLING, callback=process_kill, bouncetime=500)
        
    ButtonOff = 18 # GPIO-4 pin 7
    GPIO.setup(ButtonOff, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(ButtonOff, GPIO.FALLING, callback=powerOff, bouncetime=5)
except:
    print()
root.after(4000, ping_gateway_task, root)
root.after(5000, ping_process_task, root)
root.focus_set()
root.mainloop()
exitfunc()
#root.destroy()