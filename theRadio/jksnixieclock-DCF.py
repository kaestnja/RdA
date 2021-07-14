#!/usr/bin/python3
version=161
modulname='jksnixieclock-DCF'
import datetime
import math
import os
import socket
#gui
#https://lawsie.github.io/guizero/images/
#https://kivy.org/#home https://kivy.org/doc/stable/installation/installation-windows.html
#https://github.com/AlfonsMittelmeyer/python-gui-messaging
#https://github.com/PySimpleGUI/PySimpleGUI https://pysimplegui.readthedocs.io/en/latest/cookbook/
#https://github.com/enthought/traitsui
#https://www.wxpython.org/ https://wxwidgets.org/ https://github.com/wxFormBuilder/wxFormBuilder http://wxglade.sourceforge.net/
#https://github.com/alejandroautalan/pygubu

#tips
#https://www.python-forum.de/viewtopic.php?f=18&t=40715&p=310946#p310946
#http://www.qtrac.eu/pyqtbook.html http://www.qtrac.eu/pytips.html http://www.qtrac.eu/pygen.html
#https://www.pygame.org/news
#https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
#https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/
#to better debug: on crash enter: import pdb; pdb.pm()
#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
#https://www.python-course.eu/python3_class_and_instance_attributes.php
import sys
import time
#http://www.raspberry-pi-geek.de/Magazin/2014/01/Raspberry-Pi-als-Funkuhr-und-NTP-Stratum-1-Zeitserver
#   sudo apt-get install -y ntpdate cryptsetup
#   watch -n 1 ntpq -c as -c cv -c rv

#   ntpdate -q PTB-Zeitserver

#https://eskofier.de/projekte/modellbau/13-wetterstation-am-modellflugplatz-mit-pywws
#http://www.dl8rds.de/index.php/Dual_Source_GPS/DCF77_NTP-Server_with_AIS_and_ADS-B_receivers
#https://www.satsignal.eu/ntp/Raspberry-Pi-NTP.html
#http://www.dl3ukh.de/Bastel-Decoder.htm
#https://www.dcf77logs.de/live
#http://www.raspberry-pi-geek.de/Magazin/2014/01/Raspberry-Pi-als-Funkuhr-und-NTP-Stratum-1-Zeitserver/(offset)/2
#http://www.netzmafia.de/skripten/hardware/RasPi/index.html
#https://www.pipperr.de/dokuwiki/doku.php?id=raspberry:dcf77_modul
#http://jurameer.com/elektronik/dcf77generator/dcf77generator.html

#https://github.com/F5OEO/rpitx
## ## pip install git+https://github.com/sn4k3/FakeRPi
## python -m pip install git+https://github.com/sn4k3/FakeRPi
import importlib.util
try:
    # Check and import real RPi.GPIO library
    # sudo pip3 install --upgrade fakeRPiGPIO
    # python -m pip install --upgrade fakeRPiGPIO
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    # If real RPi.GPIO library fails, load the fake one
    """
    import FakeRPi.GPIO as GPIO
    OR
    import FakeRPi.RPiO as RPiO
    """
    import FakeRPi.GPIO as GPIO
from datetime import datetime
from datetime import timedelta
from array import *
########################################################################################
import tkinter
import traceback
from tkinter import colorchooser, font, ttk

import PIL  # pip3 install pillow  or  python -m pip install pillow or sudo apt-get install python3-pil.imagetk
from PIL import Image, ImageDraw, ImageFont, ImageTk

#pyaudio error on windows:
#pip install pipwin
#pipwin install pyaudio

if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads

###########################################################################
#from tkinter import *       #tkinter.Button
#available in ttk: Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar
#from tkinter.ttk import *  tkinter.ttk.Button
# 480x320 rpi1
#/usr/bin/convert "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_Sunscreen.png" -resize "200x200!" -quality 100 "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_SunscreenX200.png"
#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
#class Clock(object):
class Clock(tkinter.Canvas):
    width = 0
    height = 0
    path_aNixie = os.path.join(sys.path[0],'aNixie')
    Background = ''
    hx = 0
    hy = 0
    hw = 0
    hh= 0
    inconfiguremode = 0
    NumberPicsize = ''
    NumberPicFolderPath = ''
    _hours = 0
    __minutes = 0
    __seconds = 0
    dot = 0
    # Fuer Debug-Ausgabe
    DEBUG = True
    yearold = 9999
    monthold = 99
    dayold = 99
    hourold = 99

    #def __init__(self, hours, minutes, seconds):
    def __init__(self,master,*args,**kwargs):
        super(Clock,self).__init__(master,*args,**kwargs)
        print (modulname + ": self.width: %d, self.height: %d" % (self.width,self.height))
        self.width=int(self['width'])
        self.height=int(self['height'])
        print (modulname + ": self.width: %d, self.height: %d" % (self.width,self.height))
        if self is not None:
            print (modulname + ": self  : %s" % str(self))    #.!metervamainframe.!meter
        if master is not None:
            print (modulname + ": master: %s" % str(master))  #.!metervamainframe
        if args is not None:
            for value in args:
                print (modulname + ": arg: %s" % str(value))
        if kwargs is not None:
            for key, value in kwargs.items():
                print (modulname + ": kwarg: %s == %s" %(key,value))
        self.time1 = time.strftime('%H:%M:%S') ##############################----------------##
        
        self.configure(borderwidth=0,highlightthickness=0)
        self.Background = os.path.join(os.path.join(sys.path[0],'aFrame'),'template_440x220.png')
        if 0 == 0:
            self.NumberPicFolderPath = os.path.join(os.path.join(self.path_aNixie,'nixie_digits_1_0_by_jrandomnoob-d9i6tss'),'png')
            sized = (135,180)
        else:
            self.NumberPicFolderPath = os.path.join(os.path.join(self.path_aNixie,'bIN18'),'dark1')
            sized = (80,180)
        print (modulname + ": self.NumberPicFolderPath : %s" % str(self.NumberPicFolderPath ))
        #file=0.png && size= && /usr/bin/convert "/home/pi/aRadio/theRadio/aNixie/nixie_digits_1_0_by_jrandomnoob-d9i6tss/png/$file" -resize "200x200!" -quality 100 "/home/pi/aRadio/theRadio/aNixie/nixie_digits_1_0_by_jrandomnoob-d9i6tss/png/$file"
########  back
        self.imageBackground = PIL.Image.open(self.Background)
        print (modulname + ": ClockBackground width: {0}, height: {1}".format(self.imageBackground.width,self.imageBackground.height))
        self.photoBackground = tkinter.PhotoImage(file=self.Background)
########  numbers
        #size='135x180'  #165x220
        size = str(sized[0]) + 'x' + str(sized[1])
        self.path_aNixie0 = os.path.join(self.NumberPicFolderPath,'0.png')
        #Image0 width: 384, height: 512
        self.imageNixie0 = PIL.Image.open(self.path_aNixie0)
        print (modulname + ": Image0 width: {0}, height: {1}".format(self.imageNixie0.width,self.imageNixie0.height))
        self.photoNixie0 = tkinter.PhotoImage(file=self.path_aNixie0)
 
        for i in range(10):
            current_file=os.path.join(self.NumberPicFolderPath,'%i.png' %(i))
            resized_file=os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,size))
            #print (current_file)
            #print (resized_file)
            #print (os.path.join(self.NumberPicFolderPath,'%i.png' %(i)))
            #print (os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,size)))

            if not os.path.isfile(resized_file):
                #print ('/usr/bin/convert "' + current_file + '" -resize "' + size + '!"' + ' -quality 100 "' + resized_file + '"')
                if not sys.platform == "win32":
                    try:
                        #response = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                        print ('/usr/bin/convert "' + current_file + '" -resize "' + size + '!"' + ' -quality 100 "' + resized_file + '"')
                        response = os.system('/usr/bin/convert "' + current_file + '" -resize "' + size + '!"' + ' -quality 100 "' + resized_file + '"')
                        #response = os.system("ping -c 1 -l 1 -s 1 -W 1 " + ip + " > /dev/null 2>&1")
                    except:
                        print ('bad' )
                else:
                    #https://pillow.readthedocs.io/en/latest/
                    #http://pillow.readthedocs.io/en/4.2.x/handbook/tutorial.html
                    #http://pillow.readthedocs.io/en/latest/reference/Image.html?highlight=crop#PIL.Image.Image.crop
                    #https://codereview.stackexchange.com/questions/183187/crop-multiple-images-from-single-image?rq=1
                    oriImg = PIL.Image.open(current_file)
                    resizedImg = oriImg.resize(sized)
                    resizedImg.save (resized_file)
        self.imagesNixies0_9 = []
        for i in range(10):
            #print (os.path.join(self.NumberPicFolderPath,'%i.png' %(i)))
            self.imagesNixies0_9.append( PIL.Image.open( os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,size)) ) )
            #print (modulname + ": Len: %s" % str(len(self.imagesNixies0_9)))
        #self.photosNixies0_9 = [ tkinter.PhotoImage( file=os.path.join(self.NumberPicFolderPath,'%i.png' %(i)) for i in range(10)) ]
        self.photosNixies0_9 = []
        for i in range(10):
            #print (os.path.join(self.NumberPicFolderPath,'%i.png' %(i)))
            self.photosNixies0_9.append( tkinter.PhotoImage( file=os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,size)) ) )
            #print (modulname + ": Len: %s" % str(len(self.photosNixies0_9)))
######## dot
        size='135x180'  #165x220
        self.path_aNixieDot = os.path.join(self.NumberPicFolderPath,'dot.png')
        #Image0 width: 384, height: 512
        self.imageNixieDot = PIL.Image.open(self.path_aNixieDot)
        print (modulname + ": ImageDot width: {0}, height: {1}".format(self.imageNixieDot.width,self.imageNixieDot.height))
        self.photoNixieDot = tkinter.PhotoImage(file=self.path_aNixieDot)
        current_file=os.path.join(self.NumberPicFolderPath,'dot.png')
        resized_file=os.path.join(self.NumberPicFolderPath,'dot_%s.png' %(size))
        if not os.path.isfile(resized_file):
            #print ('/usr/bin/convert "' + current_file + '" -resize "' + size + '!"' + ' -quality 100 "' + resized_file + '"')
            if not sys.platform == "win32":
                try:
                    #response = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                    print ('/usr/bin/convert "' + current_file + '" -resize "' + size + '!"' + ' -quality 100 "' + resized_file + '"')
                    response = os.system('/usr/bin/convert "' + current_file + '" -resize "' + size + '!"' + ' -quality 100 "' + resized_file + '"')
                    #response = os.system("ping -c 1 -l 1 -s 1 -W 1 " + ip + " > /dev/null 2>&1")
                except:
                    print ('bad' )
        self.imageNixieDot = PIL.Image.open(resized_file)
        print (modulname + ": ImageDot width: {0}, height: {1}".format(self.imageNixieDot.width,self.imageNixieDot.height))
        self.photoNixieDot = tkinter.PhotoImage(file=resized_file)

        if (self.width==440 and self.height==220):
            self.layout()
        #self.bind("<Button 1>",self.getorigin)
        self.bind("<Button 3>",self.configuremode)
        self.set(23, 59, 59)
        self.ticker()
        
    def getBackground(self):
        return Clock.Background
    def setBackground(self,path):
        Clock.Background = path
        print (modulname + ": setAttr path: %s" % path)
        print (modulname + ": setAttr self.Background: %s" % self.Background)
        print (modulname + ": setAttr Clock.Background: %s" % Clock.Background)
        self.imageBackground = PIL.Image.open(self.Background)
        self.photoBackground = tkinter.PhotoImage(file=self.Background)
        self.layout()

    def getNumberPicFolderPath(self):
        return self.NumberPicFolderPath
    def setNumberPicFolderPath(self,path,size):
        print (modulname + ": setNumberPicFolderPath self.NumberPicFolderPath : %s" % str(self.NumberPicFolderPath ))
        print (modulname + ": setNumberPicFolderPath to: %s" % str(path))
        self.NumberPicFolderPath = path

        self.NumberPicsize=size  #'90x140'  #165x220
        self.path_aNixie0 = os.path.join(self.NumberPicFolderPath,'0.png')
        #Image0 width: 384, height: 512
        self.imageNixie0 = PIL.Image.open(self.path_aNixie0)
        print (modulname + ": Image0 width: {0}, height: {1}".format(self.imageNixie0.width,self.imageNixie0.height))
        self.photoNixie0 = tkinter.PhotoImage(file=self.path_aNixie0)

        for i in range(10):
            current_file=os.path.join(self.NumberPicFolderPath,'%i.png' %(i))
            resized_file=os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,self.NumberPicsize))
            #print (current_file)
            #print (resized_file)
            #print (os.path.join(self.NumberPicFolderPath,'%i.png' %(i)))
            #print (os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,size)))
            if not os.path.isfile(resized_file):
                #print ('/usr/bin/convert "' + current_file + '" -resize "' + size + '!"' + ' -quality 100 "' + resized_file + '"')
                if not sys.platform == "win32":
                    try:
                        #response = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                        print ('/usr/bin/convert "' + current_file + '" -resize "' + self.NumberPicsize + '!"' + ' -quality 100 "' + resized_file + '"')
                        response = os.system('/usr/bin/convert "' + current_file + '" -resize "' + self.NumberPicsize + '!"' + ' -quality 100 "' + resized_file + '"')
                        #response = os.system("ping -c 1 -l 1 -s 1 -W 1 " + ip + " > /dev/null 2>&1")
                    except:
                        print ('bad' )
            
        self.imagesNixies0_9 = []
        for i in range(10):
            #print (os.path.join(self.NumberPicFolderPath,'%i.png' %(i)))
            self.imagesNixies0_9.append( PIL.Image.open( os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,self.NumberPicsize)) ) )
            #print (modulname + ": Len: %s" % str(len(self.imagesNixies0_9)))
#        
        #self.photosNixies0_9 = [ tkinter.PhotoImage( file=os.path.join(self.NumberPicFolderPath,'%i.png' %(i)) for i in range(10)) ]
        self.photosNixies0_9 = []
        for i in range(10):
            #print (os.path.join(self.NumberPicFolderPath,'%i.png' %(i)))
            self.photosNixies0_9.append( tkinter.PhotoImage( file=os.path.join(self.NumberPicFolderPath,'%i_%s.png' %(i,self.NumberPicsize)) ) )
            #print (modulname + ": Len: %s" % str(len(self.photosNixies0_9)))
        self.layout()

    def layout(self):
        #self.configure(relief=SUNKEN)
        #self.configure(relief=RAISED)
        #self.configure(background='black')
        self.width=int(self['width'])
        self.height=int(self['height'])
        print (modulname + ": self.width: %d, self.height: %d" % (self.width,self.height))
        self.centrex = round(int(self['width'])/2)
        self.centrey = round(int(self['height'])/2)
        print (modulname + ": layout self.centrex: {0}, self.centrey: {1}".format(self.centrex,self.centrey))
        print (modulname + ": Background width: {0}, height: {1}".format(self.imageBackground.width,self.imageBackground.height))
        print (modulname + ": Background width/2: {0}, height/2: {1}".format(self.imageBackground.width/2,self.imageBackground.height/2))
        self.delete("all")
        self.create_image(self.imageBackground.width/2,self.imageBackground.height/2,image=self.photoBackground,tags='background')
        
        self.create_image(220 - 92 - 46 - 10
                #(self.imageBackground.width/2)-(self.imageNixie0.width)+(0*(self.imageNixie0.width/2))
                              ,int(round(self.imageBackground.height/2))
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[0]
                              ,tags='h10'
                              )
        self.create_image(220 - 46 - 10 
                #(self.imageBackground.width/2)-(self.imageNixie0.width)+(1*(self.imageNixie0.width/2))
                              ,int(round(self.imageBackground.height/2))
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[0]
                              ,tags='h1'
                              )
        #print (modulname + ": DotPoss x: {0}, y: {1}".format(220 - 10,int(round(self.imageBackground.height/2)) + int(round(self.imagesNixies0_9[0].height/2))))
        self.create_image(220
                #(self.imageBackground.width/2)-(self.imageNixie0.width)+(1*(self.imageNixie0.width/2))
                              #,int(round(self.imageBackground.height/2)) + int(round(self.imagesNixies0_9[0].height/2))
                              ,150
                              #,image=self.photoNixie0
                              ,image=self.photoNixieDot
                              ,tags='h1dot1'
                              )
        self.create_image(220
                #(self.imageBackground.width/2)-(self.imageNixie0.width)+(1*(self.imageNixie0.width/2))
                              #,int(round(self.imageBackground.height/2)) + int(round(self.imagesNixies0_9[0].height/2))
                              ,100
                              #,image=self.photoNixie0
                              ,image=self.photoNixieDot
                              ,tags='h1dot2'
                              )
        self.create_image(220 + 46 + 10 
                #(self.imageNixie0.width/2)+(2*(self.imageNixie0.width/2))
                              ,int(round(self.imageBackground.height/2))
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[0]
                              ,tags='m10'
                              )
                #220 + 46 + 92 + 10
        self.create_image(220 + 46 + 92 + 10
                #(self.imageNixie0.width/2)+(3*(self.imageNixie0.width/2))
                              ,int(round(self.imageBackground.height/2))
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[0]
                              ,tags='m1'
                              )

    def set(self, hours, minutes, seconds):
        if self.dot==0:
            self.dot = 1
            self.create_image(220
                    #(self.imageBackground.width/2)-(self.imageNixie0.width)+(1*(self.imageNixie0.width/2))
                                  #,int(round(self.imageBackground.height/2)) + int(round(self.imagesNixies0_9[0].height/2))
                                  ,150
                                  #,image=self.photoNixie0
                                  ,image=self.photoNixieDot
                                  ,tags='h1dot1'
                                  )
            self.create_image(220
                    #(self.imageBackground.width/2)-(self.imageNixie0.width)+(1*(self.imageNixie0.width/2))
                                  #,int(round(self.imageBackground.height/2)) + int(round(self.imagesNixies0_9[0].height/2))
                                  ,100
                                  #,image=self.photoNixie0
                                  ,image=self.photoNixieDot
                                  ,tags='h1dot2'
                                  )
        else:
            self.dot = 0
            self.delete('h1dot1')
            self.delete('h1dot2')
        self.dot = self.dot 
        if type(hours) == int and 0 <= hours and hours < 24:
            self._hours = hours
            if hours < 10:
                self.lastdigith10 = 0
            else:
                try:
                    self.lastdigith10 = int(repr(self._hours)[-2])
                except:
                    self.lastdigith10 = 0
            self.lastdigith1 = int(repr(self._hours)[-1])
            #192x256
                #440/2 = 220
                #220 - 92 - 46 - 10 - 10
            self.delete('h10')
            self.create_image(220 - 92 - 46 - 10
                #(self.imageBackground.width/2)-(self.imageNixie0.width)+(0*(self.imageNixie0.width/2))
                              ,self.imageBackground.height/2
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[self.lastdigith10]
                              ,tags='h10'
                              )
            #print (modulname + ": lastdigith10: %d at %d" % (self.lastdigith10, (self.imageBackground.width/2)-(2*(self.imageNixie0.width))))
                ##220 - 46 - 10 - 10
            self.delete('h1')
            self.create_image(220 - 46 - 10 
                #(self.imageBackground.width/2)-(self.imageNixie0.width)+(1*(self.imageNixie0.width/2))
                              ,self.imageBackground.height/2
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[self.lastdigith1]
                              ,tags='h1'
                              )
            #print (modulname + ": lastdigith1: %d at %d" % (self.lastdigith10,(self.imageBackground.width/2)-(self.imageNixie0.width)+(1*(self.imageNixie0.width/2))))
        else:
            raise TypeError(modulname + ":Stunden müssen Ganzzahlen zwischen 0 und 23 sein!")
        if type(minutes) == int and 0 <= minutes and minutes < 60:
            self.__minutes = minutes
            if minutes < 10:
                self.lastdigitm10 = 0
            else:
                try:
                    self.lastdigitm10 = int(repr(self.__minutes)[-2])
                except:
                    self.lastdigitm10 = 0
            self.lastdigitm1 = int(repr(self.__minutes)[-1])
            #print (modulname + ": lastdigitm1: %s" % str(self.lastdigitm1))
            #print (modulname + ": lastdigitm10: %s" % str(self.lastdigitm10))
                #220 + 46 + 10
            self.delete('m10')
            self.create_image(220 + 46 + 10 
                #(self.imageNixie0.width/2)+(2*(self.imageNixie0.width/2))
                              ,self.imageBackground.height/2
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[self.lastdigitm10]
                              ,tags='m10'
                              )
                #220 + 46 + 92 + 10
            self.delete('m1')
            self.create_image(220 + 46 + 92 + 10
                #(self.imageNixie0.width/2)+(3*(self.imageNixie0.width/2))
                              ,self.imageBackground.height/2
                              #,image=self.photoNixie0
                              ,image=self.photosNixies0_9[self.lastdigitm1]
                              ,tags='m1'
                              )
        else:
            raise TypeError(modulname + ":Minuten müssen Ganzzahlen zwischen 0 und 59 sein!")
        if type(seconds) == int and 0 <= seconds and seconds < 60:
            self.__seconds = seconds
        else:
            raise TypeError(modulname + ":Sekunden müssen Ganzzahlen zwischen 0 und 59 sein!")
        
    def setclockdaytime(self,h,m,s):
        #print ("%d:%02d:%02d" % (h, m, s))
        self.set(h,m,s)
    def setclockseconds(self,value):
        #self.nixieclock.set(value)
        m, s = divmod(int(value), 60)
        h, m = divmod(m, 60)
        self.setclockdaytime(h, m, s)

    def tick(self):
        if self.__seconds == 59:
            self.__seconds = 0
            if self.__minutes == 59:
                self.__minutes = 0
                if self._hours == 23:
                    self._hours = 0
                else:
                    self._hours += 1
            else:
                self.__minutes += 1
        else:
            self.__seconds += 1
        print (modulname + ": tick: {0:02d}:{1:02d}:{2:02d}".format(self._hours, self.__minutes, self.__seconds))

    def ticktick(self):
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
        if s != self.clock["text"]:
            self.clock["text"] = s
        self.after(10000, ticktick)
        
    def ticker(self):
    ##    global time  # get the current local time from the PC, if time string has changed, update it
        time2 = time.strftime('%H:%M:%S')
        if time2 != self.time1:
            self.time1 = time2
            #localtime = time.asctime( time.localtime(time.time()) )
            #print ("Local current time: %s" % str(localtime))
            #s = time.strftime('%H:%M:%S')
            #s = time.strftime('%H:%M')
            #if s != clock["text"]:
            #    clock["text"] = s
            h = int(time.strftime('%H'))
            m = int(time.strftime('%M'))
            s = 0
            self.setclockdaytime(h,m,s)
        self.after(500, self.ticker)
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
    def decodeDCF77(bit_seq):

        global DEBUG
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

        if DEBUG:
            print ("Die erkannte Zeit: " + str(hour) + ":" + str(minute) + ":XX am " + str(day) + "." + str(month) + "." + str(year))
        # Pruefen des Datums aus vorangegangenem Lauf
        if year != yearold or month != monthold or day != dayold or hour != hourold:
            if DEBUG:
                print ("ist ungleich der alten Referenzzeit: " + str(hourold) + ":XX:XX am " + str(dayold) + "." + str(monthold) + "." + str(yearold))
            yearold = year
            monthold = month
            dayold = day
            hourold = hour
            if DEBUG:
                print ("Die Referenzzeit wird auf die erkannte Zeit eingestellt und die DCF77 Auswertung wird wiederholt")
            return None
        if DEBUG:
            print ("Ist gleich der alten Referenzzeit: " + str(hourold) + ":XX:XX am " + str(dayold) + "." + str(monthold) + "." + str(yearold))

        # Umrechnen ins datetime-Format
        second = 0
        microsecond = 0
        dcf77_time = datetime(year, month, day, hour, minute, second, microsecond)
        return dcf77_time

    def clamp(self,x):
        return max(0, min(x, 255))

    def getorigin(self,eventorigin):
        self.mousex = eventorigin.x
        self.mousey = eventorigin.y
        print (self.mousex,self.mousey)
        self.itemconfigure( self.textid, text = str(self.mousex) + ' ' + str(self.mousey)   )
        self.red,self.green,self.blue = self.imageGauge.getpixel( (self.mousex, self.mousey))
        print (modulname + ": Red1: {0}, Green1: {1}, Blue1: {2}".format(self.red,self.green,self.blue))
        print (modulname + "#{0:02x}{1:02x}{2:02x}".format(self.clamp(self.red), self.clamp(self.green), self.clamp(self.blue)))
        #self.handlinefill = "#{0:02x}{1:02x}{2:02x}".format(self.clamp(self.red), self.clamp(self.green), self.clamp(self.blue))
        
    def configuremode(self,eventorigin):
        self.BackgroundPicPath0 =   os.path.join(os.path.join(sys.path[0],'aFrame'),'template_440x220.png')
        self.BackgroundPicPath1 =   os.path.join(os.path.join(os.path.join(os.path.join(sys.path[0],'aNixie'),'nixie_digits_1_0_by_jrandomnoob-d9i6tss'),'png'),'background_440x220.png')
        self.NumberPicFolderPath0 = os.path.join(os.path.join(os.path.join(sys.path[0],'aNixie'),'nixie_digits_1_0_by_jrandomnoob-d9i6tss'),'png')        #135x180
        self.NumberPicFolderPath1 = os.path.join(os.path.join(os.path.join(sys.path[0],'aNixie'),'nixie_tube_numbers__resource__by_nickpolyarush'),'png') #'90x140'
        if 0 == 1:
            self.nixieclock.set(0)
            self.nixieclock.configure(height = 220,width = 440)
            self.nixieclock.configure(borderwidth=1,highlightthickness=0)
            self.nixieclock.configure(background='orange')
            
        if self.inconfiguremode == 0:
            self.configure(borderwidth=0,highlightthickness=1)
            self.inconfiguremode = 1
            print (modulname + ": getBackground before configure: %s" % str(self.getBackground()))
            self.setBackground( path=self.BackgroundPicPath0 )
            print (modulname + ": getBackground after configure: %s" % str(self.getBackground()))

            print (modulname + ": getNumberPicFolderPath before configure: %s" % str(self.getNumberPicFolderPath()))
            self.setNumberPicFolderPath( path=self.NumberPicFolderPath0,size='135x180' )
            print (modulname + ": getNumberPicFolderPath after configure: %s" % str(self.getNumberPicFolderPath()))
        else:
            self.inconfiguremode = 0
            self.configure(borderwidth=0,highlightthickness=0)
            print (modulname + ": getBackground before configure: %s" % str(self.getBackground()))
            self.setBackground( path=self.BackgroundPicPath1 )
            print (modulname + ": getBackground after configure: %s" % str(self.getBackground()))

            print (modulname + ": getNumberPicFolderPath before configure: %s" % str(self.getNumberPicFolderPath()))
            self.setNumberPicFolderPath( path=self.NumberPicFolderPath1,size='90x140' )
            print (modulname + ": getNumberPicFolderPath after configure: %s" % str(self.getNumberPicFolderPath()))

    def exitfunc (self, event):
        quit()
        #sys.exit() #exit with exception, used to exit treads
    def exit(self, event):
        quit()
    def on_closing(self, event):
        quit()

if __name__ == '__main__':
    print (modulname + ": in main")
    root = tkinter.Tk()
    sizex = 440
    sizey = 220
    posx  = 0
    posy  = 0
    root.geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    root.bind("<Escape>", exit)

    # Hautprogramm zum Abfragen des DCF77-Signals
    # GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BOARD)
    # Pin 40 auf input und 36 auf output setzen
    GPIO.setup(40, GPIO.IN)
    GPIO.setup(36, GPIO.OUT)

    # Zustand des GPIO-Pins einlesen
    try:
        old_state = int(GPIO.input(40))
    except:
        old_state = GPIO.LOW
    
    begin_found = False
    begin_bit_found = False
    Scanning = True
    bit_seq = [int] * 59
    first_round = True
    counter = 0
    yearold = 9999
    monthold = 99
    dayold = 99
    hourold = 99

    #time1 = ''
    me = Clock(root,width=sizex,height = sizey ) #,borderwidth=0,highlightthickness=0)
    #me.grid(row=2, column=0,sticky = "nsew")
    me.place( x=posx, y=posy ) #, relwidth=1, relheight=1, anchor="nw" )
    #me.configure(borderwidth=0,highlightthickness=0)
    #me.set(0)
    root.mainloop()
    root.quit()
