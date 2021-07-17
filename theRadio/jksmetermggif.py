#!/usr/bin/python3
version=152
modulname='jk-metermg'
#to better debug: on crash enter: import pdb; pdb.pm()
import sys,os, socket, datetime, traceback
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
#maybe change from "/usr/bin/env python3" to "/usr/bin/python3"
#/usr/bin/python3 --version
#maybe pip3 install queuelib
#cd /root/aRadio/theRadio && python3 radiopy.py
#python3 /home/pi/aRadio/theRadio/janradiogrid.py
#python3 /mnt/c/____DropBox/Dropbox/aRadio/theRadio/janradiogrid.py
#python D:\__Dropbox\Dropbox\aRadio\theRadio\janradiogrid.py
#pkill -f python*
#http://snakekiller.de/download/TimeZones_Worldmap-2560x1600.jpg
#https://wiki.ubuntuusers.de/Internetradio/Stationen/

#"omxplayer -o local /home/pi/aRadio/theRadio/bImages/aRadioPicture_Text.mp4"
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '0 0 800 480'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 992 720'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 496 360'
# omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4' --win '100 100 248 180'
# omxplayer -o local 'http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/mp3/128/stream.mp3'
# DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/aRadio/theRadio/bImages/A Radio Pictures Logo 1933.mp4'
# DISPLAY=:0 /usr/bin/lxterminal -e /usr/bin/omxplayer -o local '/home/pi/Music/Asaf Avidan - One Day Live @ Sziget 2015.mp3'
########################################################################################
import tkinter
from tkinter import font, ttk, colorchooser
import PIL  #pip3 install pillow  or  python -m pip install pillow or sudo apt-get install python3-pil.imagetk
from PIL import Image, ImageTk, ImageDraw, ImageFont
###########################################################################
#from tkinter import *       #tkinter.Button
#available in ttk: Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar
#from tkinter.ttk import *  tkinter.ttk.Button
import math
#/usr/bin/convert "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_Sunscreen.png" -resize "200x200!" -quality 100 "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_SunscreenX200.png"
#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/

# class to show a gauge or panel meter
#class Clock(object):
class Meter(tkinter.Canvas):
    width = 0
    height = 0
    mousex = 0
    mousey = 0
    handcenterx = 0
    handcentery = 0
    handstartx = 0
    handstarty = 0
    handendx = 0
    handendy = 0

    configuremode = 0
    backgroundpicpath = ''

    def __init__(self,master,*args,**kwargs):
        super(Meter,self).__init__(master,*args,**kwargs)
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

        self.configure(borderwidth=0,highlightthickness=0)
        self.path_script = sys.path[0]
        self.path_aGauge = os.path.join(self.path_script,'aGauge')
        self.path_aNixie = os.path.join(self.path_script,'aNixie')
        self.path_bImages = os.path.join(self.path_script,'bImages')
        self.path_aMagicEye = os.path.join(self.path_script,'aMagicEye')
        self.path_aMagicEyes = os.path.join(self.path_aMagicEye,'BellRoss1_X185_GaugeX210_SunscreenX220_1-10_gif')

        #self.configure(relief=SUNKEN)
        #self.configure(relief=RAISED)
        #self.configure(borderwidth=0,highlightthickness=0)

        self.imageGaugeX220 = PIL.Image.open(os.path.join(self.path_aMagicEyes,'09.gif'))
        self.imageGauge = self.imageGaugeX220
        #self.imageGauge = self.imageGaugeX220.resize((240, 320))
        #self.imageGauge = self.imageGaugeX220.rotate(90).resize((240, 320))
        #self.imageGauge = PIL.ImageDraw.Draw(self.imageGaugeX220)
        #/usr/bin/convert "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_Sunscreen.png" -resize "200x200!" -quality 100 "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_SunscreenX200.png"
        print (modulname + ": Image width: {0}, height: {1}".format(self.imageGauge.width,self.imageGauge.height))

        self.photosGaugeX220 = []
        #print (modulname + ": Len1: %s" % str(len(self.photosGaugeX220)))

        #print ([os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)) for i in range(10)])
        for i in range(10):
            #print (os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)))
            self.photosGaugeX220.append( tkinter.PhotoImage( file=os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)) ) )
            #print (modulname + ": Len: %s" % str(len(self.photosGaugeX220)))

        #self.photosGaugeX220 = [ tkinter.PhotoImage( file=os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)) for i in range(10)) ]
        self.size_picture = len(self.photosGaugeX220)

        self.photoGaugeX220 = tkinter.PhotoImage(file=(os.path.join(self.path_aMagicEyes,'09.gif')))

        self.photoGauge = self.photoGaugeX220
        print (modulname + ": Photo width: {0}, height: {1}".format(self.photoGauge.width(),self.photoGauge.height()))
        #print (modulname + ":Photo width: %d, height: %d" % (self.photoGauge.width(),self.photoGauge.height()))

        #foreground='yellow'
        #self.create_image(20,20, anchor=NW, image=self.imageGauge)
        #self.create_image(int(self['height'])/2,100,image=self.imageGauge)
##        self.imagelabel = tkinter.Label(self)
##        self.imagelabel.pack()
##        self.imagelabel.configure(image=self.photoGauge)

        self.layout()
        self.graphics()

        self.setrange()
        #self.blob('yellow')

        self.bind("<Button 1>",self.getorigin)
        self.bind("<Button 3>",self.configuremode)

    def setAttr(self,attr):
        Meter.meterBackground = attr
    def getAttr(self):
        return Meter.meterBackground

    def layout(self):
        # set parameters that control the layout
        #self.configure(borderwidth=0,relief=SUNKEN)
        self.centrex = round(int(self['width'])/2)
        self.centrey = round(int(self['height'])/2)
        print (modulname + ": layout self.centrex: {0}, self.centrey: {1}".format(self.centrex,self.centrey))
        self.create_image(self.imageGauge.width/2,self.imageGauge.height/2,image=self.photoGauge)
        # standard with of lines
        self.linewidth = 2
        # outer radius for dial
        self.radius = int(round(0.40*float(self.centrex*2)))
        print (modulname + ": layout  self.radius: %s" % self.radius)
        # set width of bezel
        self.bezel = int(round(self.radius/15))
        print (modulname + ": layout  self.bezel: %s" % self.bezel)
        #self.bezelcolour1 = '#c0c0c0'
        self.bezelcolour1 = 'grey'
        #self.bezelcolour2 = '#808080'
        self.bezelcolour2 = 'green'
        # set lengths of ticks and hand
        self.majortick = int(round(self.radius/8))
        self.minortick = int(round(self.majortick/2))
        self.handlen = int(round(self.radius - self.majortick - self.bezel - 1))
        print (modulname + ": layout  self.handlen: %s" % self.handlen)
        self.blobrad = self.handlen/6
        print (modulname + ": layout  self.blobrad: %s" % self.blobrad)
        self.configure(background='black')
        
    def clamp(self,x):
        return max(0, min(x, 255))

    def graphics(self):
        # create the static components
        if 1 == 0:
            self.create_oval(self.centrex-self.radius
            ,self.centrey-self.radius
            ,self.centrex+self.radius
            ,self.centrey+self.radius
            ,width = self.bezel/2
            ,outline = self.bezelcolour2, fill = 'black')

        if 1 == 0:
            self.create_oval(self.centrex-self.radius - self.bezel
            ,self.centrey-self.radius - self.bezel
            ,self.centrex+self.radius + self.bezel
            ,self.centrey+self.radius + self.bezel
            ,width = self.bezel
            ,outline = self.bezelcolour1)#, fill = 'black')

        self.textid = self.create_text(
        self.centrex
        ,self.centrey + 1*self.blobrad
        ,fill = 'white'
        ,font = tkinter.font.Font(size = -int(self.majortick)))

        self.blobid = self.create_oval(
        self.centrex - self.blobrad
        ,self.centrey - self.blobrad
        ,self.centrex + self.blobrad
        ,self.centrey + self.blobrad
        ,outline = 'white', fill = 'green')


    def setrange(self, start = 0, end = 100):
        #print (modulname + ": setrange --------------------")
        self.start = start
        self.end = end
        self.range = end - start
        #print (modulname + ": setrange self.range: %s" % str(self.range))

    def set(self,value):
        if value <= self.start:
            picture_current = 0
        elif value >= self.end:
            picture_current = 9
        else:
            picture_current = int(round((value * self.size_picture-1) / self.range))
        if picture_current <= 0:
            picture_current = 0
        elif picture_current >= 9:
            picture_current = 9
        self.create_image(self.imageGauge.width/2,self.imageGauge.height/2,image=self.photosGaugeX220[picture_current])
        self.itemconfigure(self.textid,text = str(value))

    def blob(self,colour):
        #print (modulname + ": blob --------------------")
        # call this to change the colour of the blob
        self.itemconfigure(self.blobid,fill = colour,outline = colour)
        parent_name = self.winfo_parent()
        #print (modulname + ": parent_name: %s" % str(parent_name))
        parent = self._nametowidget(parent_name)
        #print (modulname + ": parent: %s" % str(parent))

##        if 1 == 0:
##            self.apixel = self.imageGauge.getpixel( (self.imageGauge.width/2, self.imageGauge.height/2) )
##            self.red = self.apixel[0]
##            self.green = self.apixel[1]
##            self.blue = self.apixel[2]
##        else:
##            self.red,self.green,self.blue = self.imageGauge.getpixel( (self.imageGauge.width/2, self.imageGauge.height/2) )
##        print (modulname + ": Red1: {0}, Green1: {1}, Blue1: {2}".format(self.red,self.green,self.blue))
##        self.handcolor = "#{0:02x}{1:02x}{2:02x}".format(self.clamp(self.red), self.clamp(self.green), self.clamp(self.blue))
##        print (modulname + ": createhand self.handcolor: %s' % str(self.handcolor))

    def getcenter(self):
        return self.handcenterx,self.handcentery
    def setcenter(self,x,y):
        self.handcenterx = x
        self.handcentery = y
        #print (modulname + ": setcenter x: %d, y: %d" % (self.handcenterx,self.handcentery))
    def configuremode(self,eventorigin):
        if self.configuremode == 0:
            #self.itemconfig(self.handid,fill = 'red')
            self.configuremode = 1
        else:
            #self.itemconfig(self.handid,fill = 'black')
            self.configuremode = 0
    def getorigin(self,eventorigin):
        self.mousex = eventorigin.x
        self.mousey = eventorigin.y
        #print (self.mousex,self.mousey)
##        if 'green' == self.itemcget(self.handid, "fill"):
##            self.handendx = self.mousex
##            self.handendy = self.mousey
##            self.itemconfig(self.handid,fill = 'black')
##        if 'yellow' == self.itemcget(self.handid, "fill"):
##            self.handstartx = self.mousex
##            self.handstarty = self.mousey
##            self.itemconfig(self.handid,fill = 'green')
##        if 'red' == self.itemcget(self.handid, "fill"):
##            self.handcenterx = self.mousex
##            self.handcentery = self.mousey
##            self.itemconfig(self.handid,fill = 'yellow')

if __name__ == '__main__':
    print (modulname + ": in main")
    root.mainloop()
    exitfunc()
    #root.destroy()