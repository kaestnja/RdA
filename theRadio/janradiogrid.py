#!/usr/bin/python3
# https://blogs.msdn.microsoft.com/pythonengineering/2018/04/18/python-in-visual-studio-15-7-preview-4/
version=167
modulname='janradiogrid'
remotedebug_enable = 0
gpio_exist = 0
gi_exist = 0
win32com_exist = 0
sound_exist = 0
printredirect = 0
switchexternal_touse = 0

r"""
     #/usr/bin/python3 --version
     maybe pip3 install queuelib
     cd /root/aRadio/theRadio && python3 radiopy.py
     python3 /home/pi/aRadio/theRadio/janradiogrid.py
     python3 /mnt/c/____DropBox/Dropbox/aRadio/theRadio/janradiogrid.py
     python D:\__Dropbox\Dropbox\aRadio\theRadio\janradiogrid.py
     pkill -f python*
     http://snakekiller.de/download/TimeZones_Worldmap-2560x1600.jpg
     https://wiki.ubuntuusers.de/Internetradio/Stationen/
     "omxplayer -o local /home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4"
     omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
     omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '0 0 800 480'
     omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 992 720'
     omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 496 360'
     omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 248 180'
    "omxplayer -o hdmi /home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4"
     omxplayer -o hdmi '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
     omxplayer -o hdmi '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '0 0 800 480'
     omxplayer -o hdmi '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 992 720'
     omxplayer -o hdmi '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 496 360'
     omxplayer -o hdmi '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 248 180'
     omxplayer -o hdmi 'http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
     DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
     DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/Music/Asaf Avidan - One Day Live @ Sziget 2015.mp3'
     @xterm -fn fixed /usr/bin/omxplayer '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4'
     @/usr/bin/lxterminal -e /usr/bin/omxplayer '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4'
     @DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4'
     @omxplayer '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4'
     @omxplayer -o local '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4' --win '0 0 800 480'
     @sleep 20s
     @tzclock
     @gauge
     @python3 /home/pi/aRadio/theRadio/janradiogrid.py
     To Do:
     -https://docs.microsoft.com/de-de/visualstudio/python/debugging-python-code-on-remote-linux-machines
     -http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html

 gif ani https://pypi.org/project/FBpyGIF/
sudo apt install libjpeg8-dev libfreetype6-dev libwebp-dev -y
sudo apt install python3-pip
sudo pip3 install fbpygif
test
sudo python3 -m FBpyGIF -ct
use
sudo FBpyGIF [directory or file list...]
sudo python3 -m FBpyGIF.main '/home/pi/aRadio/theRadio/bImages/aRadioPicture.gif'
sudo python3 -m FBpyGIF [...]

https://stackoverflow.com/questions/47481540/how-can-i-use-an-animated-gif-that-will-play-when-pressed-as-a-button-in-kivy


https://kivy.org/doc/stable/gettingstarted/intro.html
sudo apt-get update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel
sudo pip3 install -U Cython
sudo pip3 install git+https://github.com/kivy/kivy.git@master
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string("""
<ExampleApp>:
    orientation: "vertical"
    Button:
        text: ""
        on_press: gif.anim_delay = 0.10
        on_press: gif._coreimage.anim_reset(True)

        Image:
            id: gif
            source: 'img.gif'
            center: self.parent.center
            size: 500, 500
            allow_stretch: True
            anim_delay: -1
            anim_loop: 1
""")

class ExampleApp(App, BoxLayout):
    def build(self):
        return self

if __name__ == "__main__":
    ExampleApp().run() 

 # Installed QT binaries from http://twolife.be/raspbian/ (make sure you have qtquick1-qml-plugins installed!)
# 3.Made a test.qml file (assuming you have a gif file called load.gif): 
# Code: Select all
    # import QtQuick 2.0

     # Rectangle {
        # id: root
        # width:800
        # height:600
    # color:"#000"
        # AnimatedImage {
            # id: viewerImage
            # anchors.centerIn: parent
        # source:"load.gif"
            # fillMode:Image.PreserveAspectCrop
    # }
     # }
# 3.qmlscene -platform eglfs test.qml


##https://donjayamanne.github.io/pythonVSCodeDocs/docs/debugging_remote-debugging/
##https://docs.microsoft.com/de-de/visualstudio/python/debugging-python-code-on-remote-linux-machines
# if remotedebug_enable:
#    import ptvsd #pip3 install ptvsd
#    #ptvsd.enable_attach('my_secret') #tcp://my_secret@192.168.178.29:5678
#    ptvsd.enable_attach(secret = 'my_secret', address = ('0.0.0.0', 8080))
#    ptvsd.enable_attach(secret=None)
#    ptvsd.wait_for_attach
# to better debug: on crash enter: import pdb; pdb.pm()
# =============================================================================
# Standard Python modules
# =============================================================================
import datetime
import os
import pathlib
import socket
import subprocess
import sys
import threading
import time
import timeit
import tkinter
import traceback
import urllib
from tkinter import font, ttk
from urllib import parse

import PIL  # pip3 install --upgrade pillow numpy psutil pysftp requests urllib or  python -m pip install pillow or sudo apt-get install python3-pil.imagetk
# =============================================================================
import psutil
import pygame
import requests
from PIL import ImageTk

import jksinstall as jksinstall
import jksip as jksip
import jksmeterva as meterva
import jksmeterva_cpu as meterva_cpu
import jksnixieclock as nixieclock

if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
#from tkinter import *       #tkinter.Button
#available in ttk: Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar
#from tkinter.ttk import *  tkinter.ttk.Button
# =============================================================================
# External Python modules

if not sys.platform == "win32":
    try:
        import RPi.GPIO
        gpio_exist = 1
    except:
        print ("jk-import RPi.GPIO failed")
        traceback.print_exc()
if sys.platform == "win32":
    try:
        jksinstall.Install("pypiwin32")  # also tried 'pywin32'
        import win32com.client as wincl #import win32com #pip install pywin32 didn't work for me but pypiwin32 did
        from win32com.client import Dispatch
        win32com_exist = 1
    except:
        traceback.print_exc()
#https://docs.python.org/3/library/pathlib.html
#if sys.platform == "win32":
#    import ntpath
#    pathmodule = ntpath
#else:
#    import posixpath
#    pathmodule = posixpath
#print ('jk-pathmodule: %s' % str(pathmodule))

##except Exception as e:
##    print ("jk-import RPi.GPIO failed")
##    print (e)
#import fontconfig
#import fontTools
#from fontTools import ttLib
#http://python-gtk-3-tutorial.readthedocs.io/en/latest/
# try:
#     import gi #pip3 install PyGObject  or  python -m pip install PyGObject or sudo apt-get install ? python3-PyGObject
#     #from gi.repository import Gtk, GObject
#     #from gi.repository.Gtk import*
#     #sys.path.append('/usr/lib/python2.7/dist-packages/gi')
#     gi_exist=1
#     gi.require_version('Gdk', '3.0')
#     gi.require_version('Gtk', '3.0')
#     from gi.repository import Gdk, Gtk, GObject
# except:
#     traceback.print_exc()

# =============================================================================
# Misc Definitions
# pylint: disable=E1101
# =============================================================================
# =============================================================================
# First Class
# =============================================================================
class Sample_Class(object):

    def __init__(self,master, assign_input={}, *optional_value_input, **optional_dict_input):
        """
        Keyword Arguments:
        ------------------
        self. -> STRING: Description. Default =
        self. -> OBJECT: Description. Default = 

        Input Attributes:
        -----------------
        self. -> SCALAR: Description. Default = 

        Additional Attributes:
        ----------------------
        self. -> BOOLEAN: Description. Default = 

        Documentation last updated: Month. Day, Year - Author
        """
        self.master = master
        master.title("A simple GUI")
        # Default Values
        player_touse = ''
        # Input Checks
        # init ...
        self.attribute = assign_input

        the_hostname = socket.gethostname()
        if not ('sky' in the_hostname or 'test' in the_hostname):
            object.overrideredirect(1)
            object.wm_attributes("-topmost", True)
            self.wm_attributes("-alpha", 0.5)
            self.wm_attributes("-disabled", True)
            self.wm_attributes("-transparentcolor", "blue")
            self.withdraw()
            self.wm_attributes("-toolwindow", 1)
            self.update_idletasks()
        #root.tk_setPalette(background='#40E0D0', foreground='black',activeBackground='black', activeForeground='yellow')

        #pp([(p.pid, p.info) for p in psutil.process_iter(attrs=['name', 'status']) if p.info['status'] == psutil.STATUS_RUNNING])
        proclist = {}
        proclist = psutil.process_iter()
        for proc in proclist:
            if 'omxplayer' in proc.name():
                playertouse = proc.name()
                break
            if 'mplayer' in proc.name():
                player_touse = proc.name()
                break
            if 'wmplayer' in proc.name():
                player_touse = proc.name()
                break
            if 'MPLAYER2' in proc.name():
                player_touse = proc.name()
                break
        #process_stop_radio(player_touse)
        #todo
        #button3aclick(ButtonAnAus=22)
        if player_touse == '':
            if not sys.platform == "win32":
                try:
                    omxc = subprocess.Popen(['omxplayer', '-o','local', '--blank', '/home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4','&'])
                    #os.system('omxplayer --blank /home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4 &')
                    player_touse = 'omxplayer'
                except:
                    traceback.print_exc()
            if sys.platform == "win32" and 0 == 1 :
                try:
                    #os.system('start wmplayer "' + radio_station + '"')
                    #start /D /min wmplayer "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    #start /D C:\Programme\Windows%Media%Player /min wmplayer.exe "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    #os.system('start /D /min wmplayer "' + radio_station + '"')
                    #os.system('start /D /min wmplayer "' + radio_station + '" /SkipFUE /RemoteOCXLaunch')
                    #os.system('start wmplayer /SkipFUE /RemoteOCXLaunch "' + radio_station + '"')
                    #os.system('start MPLAYER2 /play /close "' + radio_station + '"')

                    #Import WMPLib # reference Com, Windows Media Player C:\Windows\System32\wmp.dll
                    #  then change the uiMode property to "none".  wmp.Visible=0
                    #AxWindowsMediaPlayer.URL = "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    #axWindowsMediaPlayer1.Ctlcontrols.stop();

                    #mp.Visible=0
                    #tune = mp.newMedia("C:/Program Files/Common Files/HP/Memories Disc/2.0/audio/Swing.mp3")
                    #tune = mp.newMedia("C:/WINDOWS/system32/oobe/images/title.wma")
        #            tune = mp.newMedia(str(radio_station))
                    #tune = mp.newMedia("http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3")
        #            mp.currentPlaylist.appendItem(tune)
                    #mp.URL = "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    MediaPath = os.path.join(os.path.join(sys.path[0],'bImages'), 'aRadioPicture_Text.mp4')
                    os.system('start MPLAYER2 /play /close "' + MediaPath + '"')
                    #tune = mp.newMedia(str(MediaPath.replace('//','/')))
                    #tune = mp.newMedia(str(MediaPath))
                    #mp.currentPlaylist.appendItem(tune)
                    #mp.URL = str(MediaPath)
                    #mp.URL = str(MediaPath.replace('//','/'))
                    mp.controls.play()
                    player_touse = 'MPLAYER2'
                except:
                    traceback.print_exc()

        global Beschriftungen
        Beschriftungen = ['Empfänger', 'Sender', 'Betrieb', 'Kanal', 'Frequenzkontrolle',
                          'Antennen Abstimmung', 'Antennen Kopplung', 'Taste', 'Vorheizen',
                          'Verkehrsart', 'Mithören', 'Ortstaste', 'Fernhörer', 'Modulation',
                          'Leistung', 'Laustärke','Aus','Ein', 'Grob', 'Fein', 'Hauptschalter']
        if not os.path.isdir(sys.path[0]):
            sys.exit()
        if not pathlib.Path(sys.path[0]).exists:
            sys.exit()
        if not pathlib.Path(sys.path[0]).is_dir:
            sys.exit()
        path_aGauge = os.path.join(sys.path[0],'aGauge')
        path_aNixie = os.path.join(sys.path[0],'aNixie')
        path_bImages = os.path.join(sys.path[0],'bImages')
        path_aFrame = os.path.join(sys.path[0],'aFrame')
        path_aSound = os.path.join(sys.path[0],'aSound')
        path_aMagicEye = os.path.join(sys.path[0],'aMagicEye')
        path_file_senders = os.path.join(sys.path[0], 'senderlist.txt')
        path_file_sender = os.path.join(sys.path[0], 'sender.txt')
        path_file_temp = os.path.join(sys.path[0], 'temp_' + the_hostname + '_2.txt')
        charging_trueImage = tkinter.PhotoImage(os.path.join(path_bImages,'button_true_105x42.png'))
        charging_trueImagePIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_bImages,'button_true_105x42.png'))
        charging_falseImage = tkinter.PhotoImage(os.path.join(path_bImages,'button_false_105x42.png'))
        charging_falseImagePIL = PIL.ImageTk.PhotoImage(file = os.path.join(path_bImages,'button_false_105x42.png'))
        ###########################################################################
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

        #print ('jk-printing to stdout', file = sys.stdout)
        #print ('jk-printing to stderr', file = sys.stderr)
        print ('jk-hostname: %s' % str(the_hostname))
        print ('jk-platform: %s' % str(sys.platform))
        print ('jk-Python version: %s' % str(sys.version))
        #print ('jk-Python version_info: %s' % str(sys.version_info))
        print ('jk-Python executable: %s' % str(sys.executable))
        print ('jk-Python path: %s' % str(sys.path))
        #sys.path.append("/path/to/my/module")
        #print ("jk-Python modules: %s" % str(sys.modules))
        print ('jk-sys.path[0] is %s' % sys.path[0])
        #sys.stdout.write
        #print ("jk-Python __stdin__: %s" % sys.__stdin__)
        #print ("jk-Python __stdout__: %s" % sys.__stdout__)
        #print ("jk-Python __stderr__: %s" % sys.__stderr__)
        #print ("jk-Python displayhook : %s" % sys.displayhook)
        ###########################################################################
        
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
        if (not 'radio' in the_hostname):
            taskbar_height = 100
        if (screen_height - taskbar_height > sizey):
            posy  = screen_height - taskbar_height - sizey
        # if gi_exist == 1:
        #     s = Gdk.Screen.get_default()
        #     print ("jk-screen Screen       width:%d  height:%d" % (s.get_width(),s.get_height()))
        #     # Replace w with the GtkWindow of your application
        #     w = Gtk.Window()
        #     # Get the screen from the GtkWindow
        #     s = w.get_screen()
        #     # Using the screen of the Window, the monitor it's on can be identified
        #     m = s.get_monitor_at_window(s.get_active_window())
        #     # Then get the geometry of that monitor
        #     monitor = s.get_monitor_geometry(m)
        #     # This is an example output
        #     print ("jk-screen Monitor      width:%s  height:%s" % (monitor.width, monitor.height))

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
        #https://docs.python.org/3.5/library/tkinter.ttk.html?highlight=ttk
        tkkstyle = 0
        style = tkinter.ttk.Style() #use it as style="BW.TLabel")
        style.configure("BW.TLabel"
                        #, foreground="white"
                        #, background="black"
                        )
        ###########################################################################
        clock_nixieclock = nixieclock.Clock(root,width=440,height = 220) #,borderwidth=0,highlightthickness=0)
        #clock_nixieclock.grid(row=2, column=0,sticky = "nsew")
        clock_nixieclock.place(x=0, y=0)    #, relwidth=1, relheight=1 ,anchor="nw")
        #clock_nixieclock.configure(borderwidth=0,highlightthickness=0)
        #clock_nixieclock.set(0)

        meter1 = meterva_cpu.Meter(root,width=220,height = 220)
        meter1.place(x=0, y=220)

        #meter2 = metermg.Meter(root,width=220,height = 220)
        #meter2 = meter360.Meter(root,width=220,height = 220)
        meter2 = meterva.Meter(root,width=220,height = 220)
        meter2.place(x=220, y=220)
        meter2.setrange(0,150,typetxt='cpu')
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
                                  #,command=button1aclick
                                  )
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
                                  #,command=button1bclick                               
                                  )
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
        #t2a.insert(tkinter.END, str(get_sys_class_string('/proc/cpuinfo')))
        t2a.insert(tkinter.END, str(player_touse))
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
                                  #,command=button3aclick
                                  )
        t3a.window_create(tkinter.INSERT, window=button3a)

        t3b = tkinter.Text(btframe3, background='black',foreground='blue',borderwidth=0,highlightthickness=0
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
        #t3b.tag_config('STATE', foreground='yellow')
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
                                #,relief=tkinter.FLAT
                                #,relief=tkinter.RAISED
                                #,relief=tkinter.SUNKEN
                                #,relief=tkinter.GROOVE
                                ,relief=tkinter.RIDGE       
                                ,selectmode=tkinter.SINGLE
                                ,background='black'
                                ,foreground='saddle brown'
                                ,selectforeground='orange'
                                ,selectbackground='black'
                                ,highlightcolor='saddle brown'
                                ,highlightbackground='sandy brown'
                                ,highlightthickness=0
                                ,disabledforeground='red'
                                ,activestyle='dotbox'#'none'
                                ,exportselection=False
                                ,yscrollcommand=senderscrollbar.set
                                ,font=global_font
                                #,setgrid=1
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

        #downframepicture1 = PIL.ImageTk.PhotoImage(file=os.path.join(sys.path[0] + '//aNixie','zm1080_l2_09bdm_30x50_8b [www.imagesplitter.net]-0-0.gif'))
        #root.downframepicture1 = downframepicture1
        #downframeLabel1 = Label(master=rightbottomframe, image=downframepicture1)

        #downframeCanvas1 = Canvas(rightframe)
        #downframeCanvas1.create_image((0,0),image=downframepicture,anchor='nw')

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
        dicsenders
        #for fkey, fvalue in dicsenders:
        #for key in sorted(d.keys())
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

        #subprocess.Popen(['omxplayer','-b',os.path.join(path_aNixie,'shutdown.wav')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        #https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.get_length
        #import pygame
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag #pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffersize=4096)
        try:
            pygame.mixer.init()
            sound_exist=1
        except:
            traceback.print_exc()
            sound_exist=0

        sounds = pygame.mixer
        sounds.init()

        def wait_finish(channel):
            while channel.get_busy():
                pass
        s = sounds.Sound(os.path.join(path_aSound,'on1.wav'))
        wait_finish(s.play())

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

        Rotary_counter = 0              # Start counting from 0
        Current_A = 1                   # Assume that rotary switch is not
        Current_B = 1                   # moving while we init software
        LockRotary = threading.Lock()

        if gpio_exist == 1:
            #+   - 3v3 (pin1)
            #GND - GND (pin6)
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            RPi.GPIO.setwarnings(True)
            #https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=133740
            clk2 = 23  # Encoder input A: input GPIO23 (active high) pin 16
            dt2 = 24  # Encoder input B: input GPIO24 (active high) pin 18  pull_up_down=RPi.GPIO.PUD_DOWN
            clk = 27  # Encoder input A: input GPIO23 (active high) pin 13
            dt = 17  # Encoder input B: input GPIO24 (active high) pin 11  pull_up_down=RPi.GPIO.PUD_DOWN
            if 0==1:
                RPi.GPIO.setup(clk, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
                RPi.GPIO.setup(dt, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
                # setup an event detection thread for the A encoder switch   RISING ,FALLING bouncetime=5 bouncetime in mSec
                RPi.GPIO.add_event_detect(clk, RPi.GPIO.FALLING, callback=self.switch_event)
                RPi.GPIO.add_event_detect(dt, RPi.GPIO.FALLING, callback=self.switch_event)
            else:
                RPi.GPIO.setup(clk, RPi.GPIO.IN)
                RPi.GPIO.setup(dt, RPi.GPIO.IN)
                # setup an event detection thread for the A encoder switch   RISING ,FALLING bouncetime=5 bouncetime in mSec
                RPi.GPIO.add_event_detect(clk, RPi.GPIO.RISING, callback=self.rotary_interrupt) 
                RPi.GPIO.add_event_detect(dt, RPi.GPIO.RISING, callback=self.rotary_interrupt)
            #root.after(1000, readEncoder)

            ButtonAnAus = 22 # pin 15
            #todo
            if switchexternal_touse == 1:
                RPi.GPIO.setup(ButtonAnAus, RPi.GPIO.IN)
                RPi.GPIO.add_event_detect(ButtonAnAus, RPi.GPIO.BOTH, callback=self.button3aclick, bouncetime=500)
                if GPIO.input(ButtonAnAus) == RPi.GPIO.HIGH:
                    print()
            else:
                RPi.GPIO.setup(ButtonAnAus, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
                RPi.GPIO.add_event_detect(ButtonAnAus, RPi.GPIO.FALLING, callback=self.button3aclick, bouncetime=500)
    
            ButtonOff = 18 # pin 12
            RPi.GPIO.setup(ButtonOff, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
            RPi.GPIO.add_event_detect(ButtonOff, RPi.GPIO.FALLING, callback=self.powerOff, bouncetime=5)



        ########################################################################################
        def print_to(self, temp_string):
            try:
                with open(path_file_temp,"a") as temp_file:
                    temp_file.write(temp_string + "\n")
                    print ("jk-did print_to to file: %s" % path_file_temp)
                    return 0
            except:
                traceback.print_exc()
                print ("jk-could not print_to to file: %s" % path_file_temp)
                return 1

        def process_start_radio( radio_station, player_touse):
            print ('  process_start_radio play: "%s"' % (radio_station))
            if player_touse == '':
                return False
            if not sys.platform == "win32":
                if player_touse == 'omxplayer':
                    try:
                        omxc = subprocess.Popen(['omxplayer', '-o','local', radio_station,'&'])
                        return True
                    except:
                        traceback.print_exc()
                if player_touse == 'mplayer':
                    os.system('mplayer -quiet -cache 100 ' + radio_station + ' &')
                    #omxc = subprocess.Popen('mplayer -quiet -cache 100 ' + dicsenders.get(list_value) + ' &')
                    #mswr1bw='mplayer -quiet -cache 100 http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                    #swr1bw='omxplayer -o local http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                    #omxplayer --win '100 100 500 500'
                    #https://github.com/cmus/cmus/wiki/status-display-programs
                    #'cmus http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
                    #https://opensource.com/life/16/8/3-command-line-music-players-linux
                if 0==1:
                    ps = subprocess.Popen(['omxplayer', '-o','local', radio_station], shell=True, stdout=subprocess.PIPE)
                    ps_pid = ps.pid
                    output = ps.stdout.read()
                    ps.stdout.close()
                    ps.wait()
            else:
                try:
                    #os.system('start wmplayer "' + radio_station + '"')
                    #start /D /min wmplayer "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    #start /D C:\Programme\Windows%Media%Player /min wmplayer.exe "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    #os.system('start /D /min wmplayer "' + radio_station + '"')
                    #os.system('start /D /min wmplayer "' + radio_station + '" /SkipFUE /RemoteOCXLaunch')
                    #os.system('start wmplayer /SkipFUE /RemoteOCXLaunch "' + radio_station + '"')
                    #os.system('start MPLAYER2 /play /close "' + radio_station + '"')

                    #Import WMPLib # reference Com, Windows Media Player C:\Windows\System32\wmp.dll
                    #  then change the uiMode property to "none".  wmp.Visible=0
                    #AxWindowsMediaPlayer.URL = "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    #axWindowsMediaPlayer1.Ctlcontrols.stop();

                    #mp.Visible=0
                    #tune = mp.newMedia("C:/Program Files/Common Files/HP/Memories Disc/2.0/audio/Swing.mp3")
                    #tune = mp.newMedia("C:/WINDOWS/system32/oobe/images/title.wma")
        #            tune = mp.newMedia(str(radio_station))
                    #tune = mp.newMedia("http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3")
        #            mp.currentPlaylist.appendItem(tune)
                    #mp.URL = "http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3"
                    mp.URL = str(radio_station)
                    mp.controls.play()
                    return True
                except:
                    traceback.print_exc()
            return False
        def process_stop_radio(player_touse):
            print('   stop radio')
            if not sys.platform == "win32":
                if player_touse == 'omxplayer':
                    #print('pkill omxplayer')
                    os.system('pkill omxplayer')
                if player_touse == 'mplayer':
                    #print('pkill mplayer')
                    os.system('pkill mplayer')
            else:
                if player_touse == 'wmplayer':
                    #print('TASKKILL wmplayer')
                    #os.system('TASKKILL /F /IM wmplayer.exe')
                    #os.system('taskkill /im "wmplayer.exe" /f >nul 2>&1') 
                    os.system('tasklist | find /I "wmplayer.exe" > nul && taskkill /f /im wmplayer.exe > nul')
                if player_touse == 'MPLAYER2':
                    os.system('tasklist | find /I "MPLAYER2.exe" > nul && taskkill /f /im MPLAYER2.exe > nul')
                mp.controls.stop()
                #os.system("taskkill python* && python D:\__Dropbox\Dropbox\aRadio\theRadio\janradiogrid.py"
        def process_exists( proc_name):
            #pp([(p.pid, p.info) for p in psutil.process_iter(attrs=['name', 'status']) if p.info['status'] == psutil.STATUS_RUNNING])
            proclist = psutil.process_iter()
            for proc in proclist:
                the_proc_name = ''
                the_proc_name = proc.name()
                the_proc_state = psutil.STATUS_ZOMBIE
                the_proc_state = proc.status()
                if proc_name in the_proc_name and (the_proc_state == psutil.STATUS_RUNNING or the_proc_state == psutil.STATUS_SLEEPING):
                    return True
            return False

        def get_sys_class(self, sys_class_string='/sys/class/thermal/thermal_zone0/temp'):
            tempC = 21
            if (('rpi' in socket.gethostname()) or ('radio' in socket.gethostname())):
                if '/sys/class/thermal/thermal_zone0/temp' in sys_class_string:
                    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
                else:
                    tempC = int(open(sys_class_string).read())
            return tempC

        def get_sys_class_string(self, sys_class_string='/proc/cpuinfo'):
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
        def button1aclick():
            print ('  button1aclick' )
            button1a.configure(image=charging_falseImagePIL)
            #button1a.bell()
            exitfunc()
        def button1bclick():
            print ('  button1bclick' )
            button1b.configure(image=charging_falseImagePIL)
            #button1b.bell()
        def button3aclick(ButtonAnAus=22):
            print ('  button3aclick' )
            #button3a.bell()
            #process_stop_radio()
            #if 1 == button1bpressed.get():
            #button1bpressed.set(0)
            #todo
            if switchexternal_touse == 1:
                if GPIO.input(ButtonAnAus) == RPi.GPIO.HIGH:
                    print()
                else:
                    print()
            else:
                if (str(sender_key.get('state')) == '1'):
                    print ('  ---------------state running - we stop now')
                    #process_stop_radio()
                    set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'0' )
                else:
                    print ('  ---------------state stoped - we start now')
                    #process_stop_radio()
                    #process_start_radio(dicsenders.get(str(sender_key.get('last'))))
                    set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'1' )
                #t3b.delete('1.0', tkinter.END)
                #t3b.insert(tkinter.END, "JK Radio (2018) V:%s" % str(version),'JK')
                ##t3b.delete("end-1c linestart", tkinter.END)
                #t3b.insert(tkinter.END, '\n' + dicsendershost.get(str(sender_key.get('last'))), 'STATE')
                ##t3b.insert("%d.%d" % (2, 0), '\n' + dicsendershost.get(list_value), 'STATE')
                ##if str(sender_key.get('state')) == '1':
                ##    t3b.tag_config('STATE', foreground='green')
                ##elif str(sender_key.get('state')) == '0':
                ##    t3b.tag_config('STATE', foreground='red')
                ##else:
                ##    t3b.tag_config('STATE', foreground='yellow')
        ##########################
        def exit(self, event):
            exitfunc()
        def on_closing(self):
            exitfunc()
        def exitfunc():
            process_stop_radio(player_touse)
            if sound_exist==1:
                effect_shutdown.play()
                while pygame.mixer.get_busy() == True:
                #while pygame.mixer.music.get_busy() == True:
                    continue
            if gpio_exist == 1:
                RPi.GPIO.cleanup(dt)
                RPi.GPIO.cleanup(clk)
            if printredirect:
                sys.stdout.flush()
                sys.stderr.flush()
                sys.stdout = save_stdout
                sys.stderr = save_stderr
                fh.close()
            print ('jk-This last via exitfunc 1')
            root.quit()
            print ('jk-This last via exitfunc 2')
            quit()
            print ('jk-This last via exitfunc 3')
            #sys.exit() #exit with exception, used to exit treads
            #root.destroy()


        def shortName(self, font):
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

        ####################################################################
        def info(self, title):
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
            try:
                #print('ping_requests: %s' % (str(prot + '://' + ip)))
                start_time1 = timeit.default_timer()
                start_time2 = time.clock()
                start_time3 = time.time()
                start_time4 = datetime.datetime.now()
                #http://docs.python-requests.org/en/master/user/advanced/#advanced
                #response = requests.get('http://swr-swr1-bw.cast.addradio.de')
                response = requests.get(prot + '://' + ip, timeout=0.2)
                time_response = response.elapsed
                time_diff1 = timeit.default_timer() - start_time1
                time_diff2 = time.clock() - start_time2
                time_diff3 = time.time() - start_time3
                time_diff4 = datetime.datetime.now() - start_time4
                #print('ping_requests response: %s' % (str(response)))
            except:
                traceback.print_exc()
                print('ping_requests exception from: %s' % (prot + '://' + ip))
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
            response = 0
            time_response = 0
            time_diff1 = 0
            time_diff2 = 0
            time_diff3 = 0
            time_diff4 = 0
            return retvalue
        ###########################
        def ping_gateway_task(self, root):
            ip_sender = dicsendershost.get(sender_listbox.get(sender_listbox.curselection()))
            time_sender = ping_requests(ip_sender)
            #time_sender = ping_socket(ip_sender)
            time_sender_show = time_sender

            if time_sender>150:
                time_sender_show=150
            elif time_sender<=0:
                time_sender_show=150

            meter2.set(int(time_sender_show))
            root.after(3000, ping_gateway_task, root)

        def ping_process_task(self, root):
            t3b.delete('1.0', tkinter.END)
            t3b.insert(tkinter.END, "JK Radio (2018) Vp:%s" % str(version),'JK')
            #t3b.delete("end-1c linestart", tkinter.END)
            t3b.insert(tkinter.END, '\n' + dicsendershost.get(str(sender_key.get('last'))), 'STATE')
            #t3b.insert("%d.%d" % (2, 0), '\n' + dicsendershost.get(list_value), 'STATE')
            t3b.tag_config('JK', foreground='orange')
            t3b.tag_config('STATE', foreground='blue')
            time.sleep(1)
            #if str(sender_key.get('state')) == '1':
            #    t3b.tag_config('STATE', foreground='green')
            #elif str(sender_key.get('state')) == '0':
            #    t3b.tag_config('STATE', foreground='red')
            #else:
            #    t3b.tag_config('STATE', foreground='yellow')
            if not sys.platform == "win32":
                if process_exists('omxplayer'):
                    #button3apressed.set(1)
                    #button3a.configure(image=charging_trueImagePIL)
                    t3b.tag_config('STATE', foreground='green')
                    if (str(sender_key.get('state')) == '0'):
                        process_stop_radio(player_touse)
                        set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'0' )
                elif process_exists('mplayer'):
                    #button3apressed.set(1)
                    #button3a.configure(image=charging_trueImagePIL)
                    t3b.tag_config('STATE', foreground='brown')
                    if (str(sender_key.get('state')) == '0'):
                        process_stop_radio(player_touse)
                        set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'0' )
                else:
                    #button3apressed.set(0)
                    #button3a.configure(image=charging_falseImagePIL)
                    t3b.tag_config('STATE', foreground='red')
                    if (str(sender_key.get('state')) == '1'):
                        process_stop_radio(player_touse)
                        process_start_radio(dicsenders.get(str(sender_key.get('last'))),player_touse)
            else:
                if process_exists('wmplayer'):
                    #button3apressed.set(1)
                    #button3a.configure(image=charging_trueImagePIL)
                    t3b.tag_config('STATE', foreground='green')
                    if (str(sender_key.get('state')) == '0'):
                        process_stop_radio(player_touse)
                        set_last_sender_to_file( path_file_sender, str(sender_key.get('last')),'0' )
                else:
                    #button3apressed.set(0)
                    #button3a.configure(image=charging_falseImagePIL)
                    t3b.tag_config('STATE', foreground='red')
                    if (str(sender_key.get('state')) == '1'):
                        process_stop_radio(player_touse)
                        process_start_radio(dicsenders.get(str(sender_key.get('last'))),player_touse)
            root.after(2000, ping_process_task, root)
        ####################################################################
        def onselect(self, evt):
            #todo
            #info('onselect')
            # Note here that Tkinter passes an event object to onselect()
            ##sender_listbox.focus()
            #print ('  ---------------listbox event')
            #print ('  sender_key               : "%s"' % (sender_key.get('last')))
            #print ('  listbox.get(ACTIVE)      : "%s"' % (str(sender_listbox.get(tkinter.ACTIVE))))
            #print ('  listbox.get(ANCHOR)      : "%s"' % (str(sender_listbox.get(tkinter.ANCHOR))))
            #print ('  listbox.curselection()[0]: "%s"' % (str(sender_listbox.curselection()[0])))
            w = evt.widget
            index = int(w.curselection()[0])
            list_value = w.get(index)
            if not(str(w.get(tkinter.ANCHOR)) == str(w.get(tkinter.ACTIVE))):
                w.see(index) #sender_listbox.see(index) #todo: remove here and make it permanent visible without selection needed
                #print ('  ------------------------------------------------------------- changed')
                #print ('You selected new item %d: "%s"' % (index, list_value))
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
                process_stop_radio(player_touse)
                #dicsendersping[list_value] = do_ping(dicsendershost.get(list_value))
                process_start_radio(dicsenders.get(list_value),player_touse)
                w.activate(index) #todo: activate it at the end of onselect
                w.selection_anchor(index)    #normally not needed, because allready correct
            else:
                print ('You reselected item %d: "%s" and state should be: %s' % (index, list_value, str(sender_key.get('state'))))
                button3aclick()

        def volumeUp(self):
            print ("Button volumeUp")
            mp.Volume(50) #0 to 100
            #subprocess.call("volup", shell=True)
        def volumeDown(self):
            print ("Button volumeDown")
            #subprocess.call("voldown", shell=True)
        def channelDown( channel):
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
        def channelUp( channel):
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

        def set_last_sender_to_file( path_file_sender,sender,state):
            sender_key['last'] = str(sender)
            sender_key['state'] = str(state) 
            #print ("file open to write: %s" % path_file_sender)
            with open(path_file_sender,"w") as ctemp_file:
                ctemp_file.write("last|" + str(sender) + '\n')
                ctemp_file.write("state|" + str(state) + '\n')
                return 0

        def readVolume():
            value = os.popen("amixer get PCM|grep -o [0-9]*%|sed 's/%//'").read()
            return int(value)
        def rotaryChange(self, direction):
            volume_step = 5
            volume = readVolume()
            if direction == 1:
                os.system("sudo amixer set PCM -- "+str(min(100,max(0,volume + volume_step)))+"%")
            else:
                os.system("sudo amixer set PCM -- "+str(min(100,max(0,volume - volume_step)))+"%")

        def powerOff(self, ButtonOff=4):
            #subprocess.call(['poweroff'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.call(['reboot'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        def switch_event(self, switch):
            if RPi.GPIO.input(clk):
                rotary_a = 1
            else:
                rotary_a = 0
            if RPi.GPIO.input(dt):
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

        def rotary_interrupt(self, A_or_B):
            global Rotary_counter, Current_A, Current_B, LockRotary
            Switch_A = RPi.GPIO.input(clk)
            Switch_B = RPi.GPIO.input(dt)
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


if __name__ == '__main__':
    print ('janradiogrid: in main')
    if win32com_exist == 1:
        try:
            wincl.Dispatch("SAPI.SpVoice").Speak("Hallo Lisa")
            mp = wincl.Dispatch("WMPlayer.OCX")
        except:
            traceback.print_exc()
    root = tkinter.Tk()

    # Test Parent
    parent = Sample_Class(root)
    #parent.Public_Method()

    # Test Child
    #child = Inherited_Class()
    #child.Public_Method()

    root.focus_set()
    #root.after(1000, ping_gateway_task, root)
    #root.after(2000, ping_process_task, root)
    sys.exitfunc = parent.exitfunc
    root.bind("<Escape>", exit)
    root.mainloop()
    parent.exitfunc()
    root.destroy()
