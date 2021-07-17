#!/usr/bin/python3
version=140
#to better debug: on crash enter: import pdb; pdb.pm()
#maybe change from "/usr/bin/env python3" to "/usr/bin/python3"
#/usr/bin/python3 --version
#maybe pip3 install queuelib
#cd /root/aRadio/theRadio && python3 radiopy.py
#python3 /home/pi/aRadio/theRadio/radiopy.py
#pkill -f python*
#http://snakekiller.de/download/TimeZones_Worldmap-2560x1600.jpg
#https://wiki.ubuntuusers.de/Internetradio/Stationen/
import sys
import socket
import os
import datetime
import time
import timeit
import subprocess
import platform
import struct
import pathlib
import math
#import multiprocessing
#import threading
#import re
#is_py2 = sys.version[0] == '2'
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
    quit()
########################################################################################
import tkinter #from tkinter import *
import tkinter.font
from tkinter import *
if __name__ == '__main__':
    root = Tk()
    try:
        os.system('pkill omxplayer')
    except:
        print ('  omxplayer to kill: not found' )
#root.withdraw()
#root.wm_attributes("-toolwindow", 1)
#root.update_idletasks()
#root.overrideredirect(1)
##########################
global path_script
path_script = sys.path[0]
if path_script=="":
    print ('jk-sys.path was empty! try to set a hardcoded one now')
    if sys.platform == "win32":
        if os.path.isdir("D:\__Dropbox\Dropbox\aRadio\theRadio"):
            path_script = "D:\__Dropbox\Dropbox\aRadio\theRadio"
            print ('jk-path_script set to: %s' % path_script)
    else:
        if os.path.isdir("/root/aRadio/theRadio"):
            path_script = "/root/aRadio/theRadio"
        if os.path.isdir("/home/pi/aRadio/theRadio"):
            path_script = "/home/pi/aRadio/theRadio"
        if os.path.isdir("/root/Dropbox/aRadio/theRadio"):
            path_script = "/root/Dropbox/aRadio/theRadio"
else:
    print ('jk-original sys.path will be used as path_script: %s' % path_script)
if not os.path.isdir(path_script):
    print ('jk-path_script %s is not a directory!' % path_script)
    sys.exit() #exit with exception, used to exit treads
if pathlib.Path(path_script).exists:
    if not pathlib.Path(path_script).is_dir:
        print ('jk-path_script is not dir (pathlib) %s' % path_script)
        sys.exit() #exit with exception, used to exit treads
else:
    print ('jk-path_script not exist (pathlib) %s' % path_script)
    sys.exit() #exit with exception, used to exit treads
###########################################################################
global the_hostname
the_hostname = socket.gethostname()
###########################################################################
path_file_senders = os.path.join(path_script, 'senderlist.txt')
path_file_sender = os.path.join(path_script, 'sender.txt')
path_file_temp = os.path.join(path_script, 'temp_' + the_hostname + '_2.txt')
print ('jk-path_file_temp is %s' % path_file_temp)
with open(path_file_temp,"w") as ctemp_file: ctemp_file.write(str(datetime.datetime.now())+"\n")

global printredirect
printredirect = 0
if printredirect:
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
#https://docs.python.org/3/library/pathlib.html
#if sys.platform == "win32":
#    import ntpath
#    pathmodule = ntpath
#else:
#    import posixpath
#    pathmodule = posixpath
#print ('jk-pathmodule: %s' % str(pathmodule))
##########################
def exit(event):
    exitfunc()
def on_closing():
    exitfunc()
def exitfunc():
    if printredirect:
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout = save_stdout
        sys.stderr = save_stderr
        fh.close()
    if not sys.platform == "win32":
        try:
            os.system('pkill omxplayer')
        except:
            print ('  omxplayer to kill: not found' )
    print ('jk-This last via exitfunc')
    root.quit()
    quit()
    #sys.exit() #exit with exception, used to exit treads
    #root.destroy()
sys.exitfunc = exitfunc
root.bind("<Escape>", exit)
########################################################################################
#try:
#   import queue as queue
#   from multiprocessing import Queue
#except ImportError:
#   import Queue as queue
#   print ("jk-import Queue")
try:
    import urllib.parse
    #from urllib.parse import urlsplit, urlunsplit
except ImportError:
    print ('jk-import urllib.parse failed')
try:
    import urllib.request
except ImportError:
    print ('jk-import urllib.request failed')
try:
    import requests
except ImportError:
    print ('jk-import requests failed')

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

try:
    import RPi.GPIO
except ImportError:
    print ("jk-import RPi.GPIO failed")
try:
    import fontconfig
except ImportError:
    print ("jk-import fontconfig failed")
try:
    import fontTools
    #from fontTools.ttLib import TTFont
except ImportError:
    print ('jk-import fontTools failed')
try:
    import fontTools.ttLib
    #from fontTools.ttLib import TTFont
except ImportError:
    print ('jk-import fontTools.ttLib failed')
#try:
#    import wx
#except ImportError:
#    print ("jk-import wx failed")
#from time import sleep
#from subprocess import Popen, PIPE, STDOUT
#from pathlib import Path
#from threading import Thread
#https://github.com/r0x0r/pywebview#dependencies
#try:
#    import webview
#    webview.create_window("It works, Jim!", "http://www.flowrl.com")
#    webview.create_window("It works, Jim!", "nixie/nixie.html")
#    webview.create_window("It works, Jim!", "nixie/nixie.html", width=300, height=100, resizable=True, fullscreen=False, min_size=(200, 100), strings={}, confirm_quit=False, background_color='#000')
    #webview.create_window("I", "")
    #webview.create_window("It works, Jim!", "nixie/nixie.html", width=300, height=100, resizable=True, fullscreen=False, min_size=(200, 100), strings={}, confirm_quit=False, background_color='#000')
    #webview.create_window("", "", width=30, height=10, resizable=True, fullscreen=False, min_size=(200, 100), strings={}, confirm_quit=False, background_color='#000')
    #url = "nixie/nixie.html"
    #webview.load_url(url)
    #content = ""
    #webview.load_html(content)
    #webview.load_html('<body>')
    #script = ""
    #webview.evaluate_js(script)
    #print("            webview.get_current_url: %s" % str(webview.get_current_url()))
    #webview.toggle_fullscreen()
    #webview.destroy_window()
#except ImportError:
#    print ("import webview failed")

global global_font
appHighlightFont = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
tkinter.font.families()
try:
    helv36 = tkinter.font.Font(family="Helvetica",size=36,weight="bold")
except:
    print("jk-tkinter.font.Font helv36 failed")
    helv36 = ("Helvetica", 36, "bold")
try:
    nixie22 = tkinter.font.Font(family="Nixie One",size=22,weight="bold")
except:
    print("jk-tkinter.font.Font nixie22 failed, try conservative one")
    nixie22 = ("Nixie One", 22, "bold")
#global_font=("1952 RHEINMETALL", 22, "bold")
global_font = nixie22

def print_to(temp_string):
    try:
        with open(path_file_temp,"a") as temp_file:
            temp_file.write(temp_string + "\n")
            print("jk-did print_to to file: %s" % path_file_temp)
            return 0
    except:
        print("jk-could not print_to to file: %s" % path_file_temp)
        return 1

#https://serverfault.com/questions/709546/how-to-get-local-ip-address-associated-with-default-gateway
global ip_internal
ip_internal = socket.gethostbyname(socket.gethostname())
print ('jk-my IP: %s' % str(ip_internal))

global ip_sender
ip_sender = 'snakekiller.de'

global ip_gateway
ip_gateway = '192.168.2.1'
def get_default_gateway_linux(): # import socket;import struct
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
def get_default_gateway_windows():
    if 1 == 0:
        try:
            import ctypes
        except ImportError:
            print ("jk-import ctypes failed")
        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        if is_admin():
            print ('jk-is_admin: yes')
        else:
            print ('jk-is_admin: no, try runas now...')
            # Re-run the program with admin rights __file__
            #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        try:
            import wmi
            wmi_obj = wmi.WMI()
            wmi_sql = 'select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE'
            wmi_out = wmi_obj.query( wmi_sql )
            for dev in wmi_out:
                print ("jk-IPv4Address: %s" % str(dev.IPAddress[0]))
                print ("jk-DefaultIPGateway: %s" % str(dev.DefaultIPGateway[0]))
        except ImportError:
            print ("jk-import wmi failed and not windows DefaultIPGateway possible")
#        try:
#            import win32com.client
#        except ImportError:
#            print ("jk-import win32com.client failed and not windows DefaultIPGateway possible")
#        try:
#            import wmi_client_wrapper as wmi
#        except ImportError:
#            print ("jk-import wmi_client_wrapper failed and not windows DefaultIPGateway possible")
        sys.stdout.flush()
        sys.stderr.flush()
if sys.platform == "win32":
    ip_gateway = get_default_gateway_windows()
else:
    ip_gateway = get_default_gateway_linux()
print ('jk-gateway: %s' % ip_gateway)
print("jk-----------------------------------------------------------7")
#https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
#https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=35838&start=50
alsaaudio_enabled = 0
try:
    import alsaaudio
    alsaaudio_enabled = 1
    print ("jk-import alsaaudio enabled")
#except ModuleNotFoundError:
#    print ("jk-import alsaaudio failed with ModuleNotFoundError")
except:
    print ("jk-import alsaaudio failed")
try:
    import audioop
except ImportError:
    print ("jk-import audioop failed")
try:
    #import smbus
    print ("jk-import smbus")
except ModuleNotFoundError:
    print ("jk-import smbus failed")
import numpy
try:
    import pyaudio
except:pass
import wave
def play_sound(sound):
    try:
        wf = wave.open(sound, 'rb')
        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()
        # define callback (2)
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)
        # open stream using callback (3)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)
        # start the stream (4)
        stream.start_stream()
    except wave.Error:
        print('Warning: caught wave.Error!')
def calculate_levels(data, chunk,sample_rate):
    # Convert raw data to numpy array
    data = struct.unpack("%dh"%(len(data)/2),data)
    data = numpy.array(data, dtype='h')
    # Apply FFT - real data so rfft used
    fourier=numpy.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier=numpy.delete(fourier,len(fourier)-1)
    # Find amplitude
    power = numpy.log10(numpy.abs(fourier))**2
    # Araange array into 8 rows for the 8 bars on LED matrix
    power = numpy.reshape(power,(8,chunk/8))
    matrix= numpy.int_(numpy.average(power,axis=1)/4)
    return matrix
if alsaaudio_enabled and 1 == 0:
    print('alsaaudio_enabled')
    # Set up audio
    #wavfile = wave.open('/home/pi/python_programs/NorwegianWood.wav','r')
    #sample_rate = wavfile.getframerate()
    #no_channels = wavfile.getnchannels()
    #output = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL)
    sample_rate = 44100
    no_channels = 2
    chunk = 512 # Use a multiple of 8
    data_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
    data_in.setchannels(no_channels)
    data_in.setrate(sample_rate)
    data_in.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    data_in.setperiodsize(chunk)
    while True:
        # Read data from device
        l,data = data_in.read()
        if l:
            # catch frame error
            try:
                max_vol=audioop.max(data,2)
                scaled_vol = max_vol//4680
            except audioop.error as e:
                if e.message !="not a whole number of frames":
                    raise e
    while True:
        # Read data from device
        l,data = data_in.read()
        data_in.pause(1) # Pause capture whilst RPi processes data
        if l:
            # catch frame error
            try:
                matrix=calculate_levels(data, chunk,sample_rate)
                for i in range (0,8):
                    print(i)
            except audioop.error as e:
                if e.message !="not a whole number of frames":
                    raise e
        time.sleep(0.001)
        data_in.pause(0) # Resume capture

print("jk-----------------------------------------------------------8")
def get_cpu_temp():
    if 'rpi' in the_hostname:
        tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    else:
        tempC = 21
    return tempC
print("get_cpu_temp:%d" % get_cpu_temp())

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
                name_str = record.string.decode('latin-1')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            family = name_str
        if name and family: break
    return name, family
####################################################################
#jk-screen width:480 height:320
#jk-screen width:1280 height:1024
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print("jk-screen width:%d height:%d" % (screen_width,screen_height))
posx  = 0
posy  = 0

if 'rpi1radio' in the_hostname:
    #posy = -24
    sizex = screen_width
    sizey = screen_height
    root.attributes('-fullscreen', True)
    #root.resizable(0,0)
    root.resizable(False, False)
    #root.update_idletasks()
    #root.overrideredirect(1)
    list_of_fonts = {}
    #list_of_fonts = os.popen("xlsfonts").readlines()
    list_of_fonts = fontconfig.query()
    #list_of_fonts = fontconfig.query().readlines()
    for xline in list_of_fonts:
        print(xline)
        #tt = fontTools.ttLib.TTFont(sys.argv[1])
        tt = fontTools.ttLib.TTFont(xline)
        print("Name: %s  Family: %s" % shortName(tt))
elif 'anneradio' in the_hostname:
    #posy = -24
    sizex = int(round(screen_width/3*2))
    sizey = int(round(screen_height/3*2))
    #sizex = screen_width
    #sizey = screen_height
    #root.attributes('-fullscreen', True)
    #root.resizable(0,0)
    #root.resizable(False, False)
    #root.update_idletasks()
    #root.overrideredirect(1)
else:
    sizex = 260+215
    sizey = 250+20
root.geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
#root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))#root.geometry("400x400+100+100")
print("jk-----------------------------------------------------------9")
root.configure(background='black')
root.title("unbekannt via %s" % ip_gateway + ' v:' + str(version))
####################################################################
#rightframe = tkinter.Frame(root,height=2,width=768, borderwidth=1, relief=SUNKEN)
#rightframe = tkinter.Frame(root,width=sizex/2, bd=1, relief=tkinter.SUNKEN)
rightframe = tkinter.Frame(root,width=155, borderwidth=1, relief=tkinter.SUNKEN,background='black')
rightframe.pack(side=tkinter.RIGHT,fill=tkinter.Y)

print ("relevant path: %s" % os.path.join(path_script + '//aMagicEye','6ZE11Resized200__1-10.gif'))
test_path1 = os.path.join(path_script,'aMagicEye')
print ("test_path1: %s" % test_path1)
test_path2 = os.path.join(test_path1,'6ZE11Resized200__1-10.gif')
print ("test_path2: %s" % test_path2)

imageMagicEyeFull = tkinter.PhotoImage(file=os.path.join(path_script + '//aMagicEye','6ZE11Resized200__1-10.gif'), format="gif -index 0")
#imageMagicEyeWorking = tkinter.PhotoImage(file=os.path.join(path_script + '//aMagicEye','6ZE11ResizedX.gif'), format="gif -index 3")
imageMagicEyeWorking = tkinter.PhotoImage(file=test_path2, format="gif -index 3")
imageMagicEyeEmpty = tkinter.PhotoImage(file=os.path.join(path_script + '//aMagicEye','6ZE11Resized200__1-10.gif'), format="gif -index 9")
imagesMagicEye = [tkinter.PhotoImage(file=os.path.join(path_script + '//aMagicEye','6ZE11Resized200__1-10.gif'), format = 'gif -index %i' %(i)) for i in range(10)]
imageMagicEyeTemp = tkinter.PhotoImage(file=os.path.join(path_script + '//aMagicEye','6ZE11Resized200__1-10.gif'))
imageGaugeTemp = tkinter.PhotoImage(file=os.path.join(path_script + '//aGauge','GaugeX200.png'))
imageNixie = tkinter.PhotoImage(file=os.path.join(path_script + '//aNixie//drawn//png','00.png'))
imagesmall = tkinter.PhotoImage(file=os.path.join(path_script + '//aNixie','small.png'))

root.imageMagicEyeFull = imageMagicEyeFull
root.imageMagicEyeWorking = imageMagicEyeWorking
root.imageMagicEyeEmpty = imageMagicEyeEmpty
root.imagesMagicEye = imagesMagicEye
root.imageMagicEyeTemp = imageMagicEyeTemp
root.imageGaugeTemp = imageGaugeTemp
root.imageNixie = imageNixie
root.imagesmall = imagesmall

def MagicEyeEmptyFullEmpty(ind):
    print (' ind: "%s"' % ind)
    time.sleep(1)
    imagetemp = imagesMagicEye[ind]
    ind += 1
    imagelabel.configure(image=imagetemp)
    if ind < 9:
        rightframe.after(200, MagicEyeEmptyFullEmpty, ind)
def MagicEyeEmptyFull(ind,currentlabel,currentframe):
    imagetemp = imagesMagicEye[ind]
    ind += 1
    currentlabel.configure(image=imagetemp)
    if ind < 9:
        currentframe.after(200, MagicEyeEmptyFull, ind,currentlabel,currentframe)
def MagicEyeFullEmpty(ind,currentlabel,currentframe):
    imagetemp = imagesMagicEye[ind]
    ind += 1
    currentlabel.configure(image=imagetemp)
    if ind < 9:
        currentframe.after(200, MagicEyeFullEmpty, ind,currentlabel,currentframe)
def MagicEyeFull(currentlabel):
    imagetemp = imagesMagicEye[0]
    currentlabel.configure(image=imagetemp)
def MagicEyeWorking(currentlabel):
    imagetemp = imagesMagicEye[6]
    currentlabel.configure(image=imagetemp)
def MagicEyeEmpty(currentlabel):
    imagetemp = imagesMagicEye[9]
    currentlabel.configure(image=imagetemp)

imagelabel = tkinter.Label(rightframe)
imagelabel.pack()
imagelabel.configure(image=imageMagicEyeWorking)
#img.place(x=250, y=250, anchor="center")
#img.place(x=0, y=0,anchor="center")
#rightframe.after(0, MagicEyeEmptyFullEmpty, 0)
#rightframe.after(0, MagicEyeEmptyFull, 0,imagelabel,rightframe)
#rightframe.after(0, MagicEyeFullEmpty, 9,imagelabel,rightframe)

downframepicture1 = tkinter.PhotoImage(file=os.path.join(path_script + '//aNixie//zm1080_l2_09bdm_30x50_8b//gif','zm1080_l2_09bdm_30x50_8b [www.imagesplitter.net]-0-0.gif'))
root.downframepicture1 = downframepicture1
downframepicture2 = tkinter.PhotoImage(file=os.path.join(path_script + '//aNixie//zm1080_l2_09bdm_30x50_8b//gif','zm1080_l2_09bdm_30x50_8b [www.imagesplitter.net]-0-1.gif'))
root.downframepicture2 = downframepicture2
downframepicture3 = tkinter.PhotoImage(file=os.path.join(path_script + '//aNixie//zm1080_l2_09bdm_30x50_8b//gif','zm1080_l2_09bdm_30x50_8b [www.imagesplitter.net]-0-11.gif'))
root.downframepicture3 = downframepicture3
downframepicture4 = tkinter.PhotoImage(file=os.path.join(path_script + '//aNixie//zm1080_l2_09bdm_30x50_8b//gif','zm1080_l2_09bdm_30x50_8b [www.imagesplitter.net]-0-2.gif'))
root.downframepicture4 = downframepicture4
downframepicture5 = tkinter.PhotoImage(file=os.path.join(path_script + '//aNixie//zm1080_l2_09bdm_30x50_8b//gif','zm1080_l2_09bdm_30x50_8b [www.imagesplitter.net]-0-3.gif'))
root.downframepicture5 = downframepicture5

#rightrightframe = Frame(root,width=155, borderwidth=1, relief=SUNKEN,background='black')
#rightrightframe.pack(side=RIGHT,fill=Y)
downframeLabel1 = tkinter.Label(master=rightframe, image=downframepicture1)
downframeLabel2 = tkinter.Label(master=rightframe, image=downframepicture2)
downframeLabel3 = tkinter.Label(master=rightframe, image=downframepicture3)
downframeLabel4 = tkinter.Label(master=rightframe, image=downframepicture4)
downframeLabel5 = tkinter.Label(master=rightframe, image=downframepicture5)
try:
    downframeLabel1.pack(side=tkinter.LEFT)
    downframeLabel2.pack(side=tkinter.LEFT)
    downframeLabel3.pack(side=tkinter.LEFT)
    downframeLabel4.pack(side=tkinter.LEFT)
    downframeLabel5.pack(side=tkinter.LEFT)
except:
    print ("downframeLabel failed")

#downframeCanvas1 = tkinter.Canvas(rightframe)
#downframeCanvas2 = tkinter.Canvas(rightframe)
try:
    downframeCanvas1.pack(side=tkinter.LEFT)
    downframeCanvas1.create_image((0,0),image=downframepicture,anchor='nw')
    downframeCanvas2.pack(side=tkinter.RIGHT)
    downframeCanvas2.create_image((0,0),image=downframepicture,anchor='ne')
except:
    print ("downframeCanvas failed")
####################################################################
#ip_gateway_ping_string = tkinter.StringVar()
#BooleanVar DoubleVar IntVar
#someVar = IntVar(name="Name of someVar")
#ip_gateway_ping_string.set(root.title())
#def changeTitle(*args):
#    # 'Name of someVar',index if a list,operation like 'w' or 'r' or 'u',
#    tempstring = str(ip_gateway_ping_string.get())
#    temptitle = root.title()
#    print ('changeTitle read ip_gateway_ping_string: "%s"' % tempstring)
#    print ('changeTitle read root.title: "%s"' % temptitle)
#    root.title(ip_gateway_ping_string.get())
##################################
#def ip_gateway_ping_updateoptions(*args):
#    tempstring = str(ip_gateway_ping_string.get())
#    temptitle = root.title()
#    print ('ip_gateway_ping_updateoptions read ip_gateway_ping_string: "%s"' % tempstring)
#    print ('ip_gateway_ping_updateoptions read root.title: "%s"' % temptitle)
#    if not tempstring in temptitle:
#        print (' variable_a diffrent strings')
#        if 'getrennt' in tempstring:
#            print ('  variable_a in getrennt')
#            #root.wm_title("getrennt")
#        elif 'verbunden' in tempstring:
#            print ('  variable_a in verbunden')
#            #root.wm_title('verbunden')
#        else:
#            print ('  variable_a in unbekannt')
#            #root.title("unbekannt")
#        changeTitle()
##################################
#ip_gateway_ping_string.trace('w', changeTitle)
#e = Entry(root, textvariable=ip_gateway_ping_string)
#e.pack()
####################################################################
#prepare the sender list as dictionary
dicsenders = {}
dicsendershost = {}
dicsendersip = {}
dicsendersping = {}
sender_key = {}
sender_key['last'] = 'off'
def get_senders_from_file(temp_path_file_senders,temp_dicsenders,temp_dicsendershost,temp_dicsendersip,temp_dicsendersping):
    file_senders = pathlib.Path(temp_path_file_senders)
    if file_senders.is_file():
        print ("file open: %s" % temp_path_file_senders)
        with open(temp_path_file_senders,"r") as atemp_file:
            for aline in atemp_file:
                if not aline.startswith('#') and not aline.startswith('version') and aline.strip():
                    (akey, avalue) = aline.split("|")
                    print ("akey: %s  avalue: %s" % (akey,avalue))
                    #print("key: %s" % key)
                    #print("value: %s" % value)
                    temp_dicsenders[akey] = avalue.strip('\n')
                    temp_host = urllib.parse.urlsplit(avalue)
                    temp_ip = socket.gethostbyname(temp_host.hostname)
                    #print ('  url[1]: "%s"' % (temp_host[1]))
                    temp_dicsendershost[akey] = temp_host.hostname
                    temp_dicsendersip[akey] = temp_ip
                    temp_dicsendersping[akey] = 0
        return 0
    else:
        print ("file not found: %s" % temp_path_file_senders)
        return 1
response = get_senders_from_file(path_file_senders,dicsenders,dicsendershost,dicsendersip,dicsendersping)
def get_last_sender_from_file(temp_path_file_sender, temp_dicsenders,temp_sender_key):
    file_sender = pathlib.Path(temp_path_file_sender)
    if file_sender.is_file():
        print ("file open: %s" % temp_path_file_sender)
        with open(temp_path_file_sender,"r") as btemp_file:
            for bline in btemp_file:
                if not bline.startswith('#') and bline.strip():
                    #print("bline: %s" % bline)
                    (bkey, bvalue) = bline.split("|")
                    if bvalue in temp_dicsenders:
                        temp_sender_key['last'] = bvalue
                        print("sender_key: %s" % temp_sender_key.get('last'))
                        return 0
                        break
    return 1
response = get_last_sender_from_file(path_file_sender,dicsenders,sender_key)
def set_last_sender_to_file(temp_path_file_sender,temp_sender_key,temp_list_value):
    temp_sender_key['last'] = temp_list_value
    file_sender = pathlib.Path(temp_path_file_sender)
    if file_sender.is_file():
        print ("file open to write: %s" % temp_path_file_sender)
        with open(temp_path_file_sender,"w") as btemp_file:
            btemp_file.write("last|" + temp_list_value)
            return 0
    return 1
####################################################################
def info(title):
    print (title)
    print ('module name:', __name__)
    print ('parent process:', os.getppid())
    print ('process id:', os.getpid())
####################################################################
def do_ping(ip):
    address = [ip]
    retvalue = 1
    if sys.platform == "win32":
        #response = os.system("ping -n 1 -l 1 -w 100 " + ip + ">nul")
        #response = os.system("cmd /c START /MIN cmd /k ( ping -n 1 -l 1 -w 100 " + ip + " )")
        response = 0
        if response == 0:
            retvalue = 0
        else:
            retvalue = 1
        ping_args = ["ping", "-n", "1", "-l", "1", "-w", "100"]
        try:
            ping = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
            out, error = ping.communicate()
            printout = str(out)
            if printout.find('TTL') != -1:
                retvalue = 0
            elif 'ttl' in printout:
                retvalue = 0
            else:
                retvalue = 1
        except:
            retvalue = 1
    else:
        #ping_args = ["ping", "-c", "1", "-l", "1", "-s", "1", "-W", "1"]
        #ping = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        response = os.system("ping -c 1 -l 1 -s 1 -W 1 " + ip + " > /dev/null 2>&1")
        #response = os.system("ping -c 1 -w2 " + ip + " > /dev/null 2>&1")
        if response == 0:
            retvalue = 0
        else:
            retvalue = 1
    return retvalue

#####################################################################
global time_sender
time_sender = 900
def ping_gateway_task(imagelabeltemp,rightframetemp,time_sender):
    time_old = time_sender
##    try:
##        start_time = time.time()
##        #response = requests.get('https://testserver.mydomain.com/service')
##        response = requests.get('https://' + ip_sender)
##        time_sender = time.time() - start_time
##    except:
##        time_sender = 0
##    print ("time s: %s" % str(time_sender))
    try:
        #start_time = time.time()
        start_time = datetime.datetime.now()
        #response = requests.get('https://testserver.mydomain.com/service')
        response = requests.get('http://' + ip_sender)
        #time_sender = time.time() - start_time
        end_time = datetime.datetime.now() - start_time
        #print int(round(time_sender.microseconds / 1000))
        #print ("time1  : %s" % str(int(round(time_sender.microseconds / 1000))))
        #print ("time2  : %s" % str(response.elapsed))
        #print ("time3  : %s" % str(int(round(response.elapsed.microseconds / 1000))))
        time_current = int(round(response.elapsed.microseconds / 1000))
    except:
        time_sender = 900
    #print ("time  : %s" % str(time_sender))

    time_sender = time_current

    time_min=10
    time_max=300
    picture_min=0
    picture_max=len(imagesMagicEye)-1
    size_time = time_max - time_min
    size_picture = picture_max - picture_min
    picture_old = 0
    picture_current = picture_max
    direction_steps = 1
    if  ((time_current > time_min and time_current < time_max) and (time_old > time_min and time_old < time_max)):
        #von normal - nach normal
        picture_old = int(round((time_old * size_picture) / size_time))
        picture_current = int(round((time_current * size_picture) / size_time))
        if picture_old>picture_current:
            direction_steps=-1
    elif ((time_current > time_min and time_current < time_max) and (time_old > time_max)):
        #von unterbrochen - nach normal
        picture_old = picture_max
        picture_current = int(round((time_current * size_picture) / size_time))
        direction_steps=-1
    elif ((time_current  > time_max) and (time_old > time_min and time_old < time_max)):
        #von normal - nach unterbrochen
        picture_old = int(round((time_old * size_picture) / size_time))
        picture_current = picture_max
    else:
        picture_old = picture_max
        picture_current = picture_max
    for i in range(picture_old,picture_current,direction_steps):
        #print (i)
        time.sleep(0.2)
        imagelabeltemp.configure(image=imagesMagicEye[i])
        #rightframetemp.after(500, MagicEyeFullEmpty, 9,imagelabeltemp,rightframetemp)


    rightframetemp.after(0, MagicEyeWorking,imagelabeltemp)
    #ip_gateway_ping_temp = do_ping(ip_gateway)
    ip_gateway_ping_temp = 0
    temp_root_title = str(root.title())
##    if temp_root_title.find('getrennt') != -1:
##        if ip_gateway_ping_temp == 0:
##            rightframetemp.after(0, MagicEyeEmptyFull, 0,imagelabeltemp,rightframetemp)
##        else:
##            rightframetemp.after(2000, MagicEyeEmpty,imagelabeltemp)
##    elif temp_root_title.find('verbunden') != -1:
##        if ip_gateway_ping_temp == 0:
##            rightframetemp.after(2000, MagicEyeFull,imagelabeltemp)
##        else:
##            rightframetemp.after(0, MagicEyeFullEmpty, 9,imagelabeltemp,rightframetemp)
    #if ip_gateway_ping_temp == 0:
    if  (time_current > time_min and time_current < time_max):
        root.title("verbunden via %s" % str(ip_gateway) + ' v:' + str(version) + ' ' + ' time: ' + str(time_sender) + ' ' + str(ip_sender))
    else:
        if temp_root_title.find('getrennt') != -1:
            time.sleep(10)
            if 1 == 0:
                if not sys.platform == "win32":
                    response = 1
                    response = os.system('lsmod | grep -E "(rtl|8712)"')
                    if response == 0:
                        root.title("probiere v:%s" % str(version))
                        #os.system("sudo modprobe -r r8712u && sudo modprobe r8712u")
                        os.system("sudo modprobe -r r8712u > /dev/null 2>&1")
                        time.sleep(15)
                        os.system("sudo modprobe r8712u > /dev/null 2>&1")
                        time.sleep(30)
        else:
            root.title("getrennt via %s" % str(ip_gateway) + ' v:' + str(version) + ' ' + ' time: ' + str(time_sender) + ' ' + str(ip_sender))
    #rightframe.after(0, MagicEyeEmptyFullEmpty, 0)
    # To iterate through the entire gif
    root.after(2000, ping_gateway_task,imagelabeltemp,rightframetemp,time_sender)  # reschedule event in 4 seconds
#####################################################################
pin = 1
if pin:
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    BUTTON_CU = 4
    BUTTON_CD = 17
    BUTTON_VU = 18
    BUTTON_VD = 22
    RELAIS_ON = 23
    RELAIS_OFF = 24
else:
    RPi.GPIO.setmode(RPi.GPIO.BOARD)
    BUTTON_CU = 7
    BUTTON_CD = 11
    BUTTON_VU = 12
    BUTTON_VD = 15
    RELAIS_ON = 16
    RELAIS_OFF = 18
if not sys.platform == "win32":
    try:
        print("GPIO.setup set here")
        #RPi.GPIO.setup(BUTTON_VU, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        #RPi.GPIO.setup(BUTTON_VD, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        #RPi.GPIO.setup(BUTTON_CU, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_OFF)
        #RPi.GPIO.setup(BUTTON_CD, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        #RPi.GPIO.setup(RELAIS_ON, RPi.GPIO.OUT)
        #RPi.GPIO.setup(RELAIS_OFF, RPi.GPIO.OUT)
    except:
        print("GPIO.setup not possible")
####################################################################
def onselect(evt):
    #info('onselect')
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    list_value = w.get(index)
    #print ('You selected item %d: "%s"' % (index, list_value))
    list_anchor = sender_listbox.get(tkinter.ANCHOR)
    #print ('You selected anchor: "%s"' % (list_anchor))
    if 'close' in list_value:
        if not sys.platform == "win32":
            try:
                os.system('pkill omxplayer')
            except:
                print ('  omxplayer to kill: not found' )
        quit()
    elif 'off' in list_value:
        if not sys.platform == "win32":
            try:
                os.system('pkill omxplayer')
            except:
                print ('  omxplayer to kill: not found' )
    elif 'reset' in list_value:
        if not sys.platform == "win32":
            try:
                os.system('pkill omxplayer')
            except:
                print ('  omxplayer to kill: not found' )
            os.system("sudo pkill -f python* && python3 /home/pi/aRadio/theRadio/radiopysmall.py")
    elif 'reboot' in list_value:
        if not sys.platform == "win32":
            os.system('pkill omxplayer')
            #os.system('sudo shutdown -r now')
            #os.system('sudo reboot')
            os.system("sudo reboot > /dev/null 2>&1")
    elif list_value in sender_key:
        ip_sender = dicsendershost.get(list_value)
        print ("ip_sender 1:%s" % str(ip_sender))
        #dicsendersping[list_value] = do_ping(dicsendershost.get(list_value))
        print ("dicsendersping 1:%s" % str(dicsendersping[list_value]))
        #if dicsendersping.get(list_value) == 0:
        #    w.itemconfig(index, foreground='yellow')
        #else:
        #    w.itemconfig(index, foreground='red')
    else:
        ip_sender = dicsendershost.get(list_value)
        print ("ip_sender 2:%s" % str(ip_sender))
        if not sys.platform == "win32":
            try:
                os.system('pkill omxplayer')
            except:
                print ('  omxplayer to kill: not found' )
        response = set_last_sender_to_file(path_file_sender,sender_key,list_value)
        #dicsendersping[list_value] = do_ping(dicsendershost.get(list_value))
        if not sys.platform == "win32":
            if dicsendersping.get(list_value) == 0:
                #mswr1bw='mplayer -quiet -cache 100 http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                #swr1bw='omxplayer -o local http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                #omxplayer --win '100 100 500 500'
                try:
                    omxc = subprocess.Popen(['omxplayer', '-o','local', dicsenders.get(list_value)])
                    #w.itemconfig(index, foreground='green')
                    print ('  play: "%s"' % (dicsenders.get(list_value)))
                except:
                    print ('  omxplayer: not found' )
                    #w.itemconfig(index, foreground='red')
####################################################################
#def on_closing():
#    if not sys.platform == "win32":
#        try:
#            os.system('pkill omxplayer')
#        except:
#            print ('  omxplayer to kill: not found' )
#    quit()
#    root.destroy()
def volumeUp():
    print("Button volumeUp")
    #subprocess.call("volup", shell=True)
def volumeDown():
    print("Button volumeDown")
    #subprocess.call("voldown", shell=True)
def channelUp(channel):
    print("Button channelUp")
    selection_indices = sender_listbox.curselection()
    # default next selection is the beginning
    next_selection = 0
    # make sure at least one item is selected
    if len(selection_indices) > 0:
        # Get the last selection, remember they are strings for some reason so convert to int
        last_selection = int(selection_indices[-1])
        # clear current selections
        sender_listbox.selection_clear(selection_indices)
        # Make sure we're not at the last item
        if last_selection < sender_listbox.size() - 1:
            next_selection = last_selection + 1
        sender_listbox.activate(next_selection)
        sender_listbox.selection_set(next_selection)
        sender_listbox.event_generate("<<ListboxSelect>>")
def channelDown():
    print("Button channelDown")
    selection_indices = sender_listbox.curselection()
    # default next selection is the end
    next_selection = sender_listbox.size()
    # make sure at least one item is selected
    if len(selection_indices) > 0:
        # Get the last selection, remember they are strings for some reason so convert to int
        last_selection = int(selection_indices[-1])
        # clear current selections
        sender_listbox.selection_clear(selection_indices)
        # Make sure we're not at the last item
        if last_selection > 0:
            next_selection = last_selection - 1
        sender_listbox.activate(next_selection)
        sender_listbox.selection_set(next_selection)
        sender_listbox.event_generate("<<ListboxSelect>>")
####################################################################
#http://effbot.org/tkinterbook/tkinter-hello-again.htm
#allways try to change:   Button(frame, text="Hello", command=self.hello).pack(side=LEFT)
#to this two lines:
#w = Button(frame, text="Hello", command=self.hello)
#w.pack(side=LEFT)
#root.protocol("WM_DELETE_WINDOW", on_closing)

senderlistboxframe = tkinter.Frame(root, relief=tkinter.SUNKEN,background='black')
#rightframe = Frame(root,width=155, borderwidth=1, relief=SUNKEN,background='black')


#senderlistboxframe.geometry('200x200')
#highlightbackground='black'
senderscrollbar = tkinter.Scrollbar(senderlistboxframe,troughcolor='black', background='saddle brown',activebackground='sandy brown')
senderscrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
#https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
#http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/listbox.html
#sender_listbox.grid(row = 0, column = 0)

sender_listbox = tkinter.Listbox(senderlistboxframe, background='black',foreground='saddle brown', selectforeground='orange',
                         selectbackground='black', highlightcolor='saddle brown', highlightbackground='sandy brown',
                         disabledforeground='red', activestyle='none', exportselection=0,
                         yscrollcommand=senderscrollbar.set,font=global_font, height=6, width=40)

#font="Helvetica 22 bold"
#font=("Helvetica", 10, "bold italic")
#font=("1952 RHEINMETALL", 22, "bold")
#sender_listbox.place(x=0,y=0)
#sender_listbox.pack(side=LEFT, fill=Y)
sender_listbox.pack(side=tkinter.LEFT,fill="both", expand=tkinter.YES)
#sender_listbox.pack(side=LEFT)
#sender_listbox.pack(pady=20)
senderscrollbar.config(command=sender_listbox.yview)

#senderlistboxframe.pack()
senderlistboxframe.pack(side=tkinter.LEFT,fill="both",expand=tkinter.YES)

sender_listbox.delete(0, END)
sender_listbox.insert(END, "reset")
sender_listbox.insert(END, "off")
temp_list = list(dicsenders.keys())
temp_list.sort(key=str.lower)
for item in temp_list:
    #print (' item key: "%s"' % item)
    sender_listbox.insert(tkinter.END, item)
#len_max = 0
#list_items = ["item2", "item2", "item3+a few characters for the size"]
#for m in list_items:
#    if len(m) > len_max:
#        len_max = len(m)
#for i in range(20):
#    sender_listbox.insert(tkinter.END, i)
sender_listbox.insert(END, "close")
sender_listbox.insert(END, "reboot")
# attach sender_listbox to scrollbar
sender_listbox.config(yscrollcommand=senderscrollbar.set)
senderscrollbar.config(command=sender_listbox.yview)
sender_listbox.bind('<<ListboxSelect>>', onselect)
sender_listbox.focus()
####################################################################
selection_to_set_key = sender_key.get('last')
print ('  selection_to_set_key: "%s"' % (selection_to_set_key))
#list(dicsenders.keys()).index("c")
#temp_list =list(dicsenders.keys())
#temp_list.sort(key=str.lower)
#selection_to_set_key_index = list(dicsenders.keys()).index(selection_to_set_key)
selection_to_set_key_index = temp_list.index(selection_to_set_key)
print ('  selection_to_set_key_index: "%d"' % (selection_to_set_key_index))
if selection_to_set_key_index >= 0 and selection_to_set_key_index <= sender_listbox.size() - 1:
    selection_to_set_key_index = selection_to_set_key_index + 1
else:
    selection_to_set_key_index = 0
sender_listbox.activate(selection_to_set_key_index)
sender_listbox.selection_anchor(selection_to_set_key_index)
sender_listbox.selection_set(selection_to_set_key_index)
#sender_listbox.selection_set(first=1)
#sender_listbox.activate(1)
#sender_listbox.selection_anchor(1)
#print ('  Your first anchor: "%s"' % (sender_listbox.get(ANCHOR)))
#print ('  size (line count): "%s"' % (sender_listbox.size()))
####################################################################
sender_listbox.event_generate("<<ListboxSelect>>")
#sender_listbox.select_set(3)
#items = map(int, list.curselection())
#index = sender_listbox.curselection()
#event = sender_listbox.get(index)

if not sys.platform == "win32":
    try:
        print("RPi.GPIO.add_event_detect set here")
        #RPi.GPIO.add_event_detect(BUTTON_VU, RPi.GPIO.FALLING, callback=volumeUp, bouncetime=600)
        #RPi.GPIO.add_event_detect(BUTTON_VD, RPi.GPIO.FALLING, callback=volumeDown, bouncetime=600)
        #RPi.GPIO.add_event_detect(BUTTON_CU, RPi.GPIO.RISING, callback=channelUp, bouncetime=600)
        #RPi.GPIO.add_event_detect(BUTTON_CD, RPi.GPIO.FALLING, callback=channelDown, bouncetime=600)
    except:
        print("RPi.GPIO.add_event_detect not possible")

time.sleep(3)
root.focus_set()
root.after(1000, ping_gateway_task,imagelabel,rightframe,time_sender)
root.mainloop()
if not sys.platform == "win32":
    try:
        os.system('pkill omxplayer')
    except:
        print ('  omxplayer to kill: not found' )
quit()
#root.destroy()
