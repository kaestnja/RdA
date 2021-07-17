#!/usr/bin/python3
import sys,os
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
import tkinter
from tkinter import font, ttk, colorchooser
#import tkinter.font
#import tkinter.ttk
#import tkinter.colorchooser
import PIL  #pip3 install pillow  or  python -m pip install pillow
import PIL.ImageTk
#from PIL import Image, ImageTk
#from tkinter import *       #tkinter.Button
#available in ttk: Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar
#from tkinter.ttk import *  tkinter.ttk.Button
#/usr/bin/convert "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_Sunscreen.png" -resize "200x200!" -quality 100 "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_SunscreenX200.png"
#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
# class to show a gauge or panel meter

#https://www.python-kurs.eu/python3_funktionen.php

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
        #print("jk-metermg: self.width: %d, self.height: %d" % (self.width,self.height))
        self.width=int(self['width'])
        self.height=int(self['height'])
        #print("jk-metermg: self.width: %d, self.height: %d" % (self.width,self.height))
        if self is not None:
            print ("jk-metermg self  : %s" % str(self))    #.!metervamainframe.!meter
        if master is not None:
            print ("jk-metermg master: %s" % str(master))  #.!metervamainframe
        if args is not None:
            for value in args:
                print ("jk-metermg arg: %s" % str(value))
        if kwargs is not None:
            for key, value in kwargs.items():
                print ("jk-metermg kwarg: %s == %s" %(key,value))
                if 'backgroundpicpath'  in key:
                    self.backgroundpicpath = value
                    print("jk-metermg: self.backgroundpicpath: %s" % self.backgroundpicpath)

        self.path_script = sys.path[0]
        self.path_aGauge = os.path.join(self.path_script,'aGauge')
        self.path_aNixie = os.path.join(self.path_script,'aNixie')
        self.path_bImages = os.path.join(self.path_script,'bImages')
        self.path_aMagicEye = os.path.join(self.path_script,'aMagicEye')
        self.path_aMagicEyes = os.path.join(self.path_aMagicEye,'BellRoss1_X185_GaugeX210_SunscreenX220_1-10_gif')
        
        #self.configure(relief=RAISED)
        #self.configure(borderwidth=0,highlightthickness=0)

        self.imageGaugeX220 = PIL.Image.open(os.path.join(self.path_aMagicEyes,'09.gif'))
        self.imageGauge = self.imageGaugeX220
        #print("jk-metermg: Image width: {0}, height: {1}".format(self.imageGauge.width,self.imageGauge.height))

        self.photosGaugeX220 = []
        #print ("jk-metermg: Len1: %s" % str(len(self.photosGaugeX220)))
        
        #print ([os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)) for i in range(10)])
        for i in range(10):
            #print (os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)))
            self.photosGaugeX220.append( tkinter.PhotoImage( file=os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)) ) )
            #print ("jk-metermg: Len: %s" % str(len(self.photosGaugeX220)))
                    
        #self.photosGaugeX220 = [ tkinter.PhotoImage( file=os.path.join(self.path_aMagicEyes,'0%i.gif' %(i)) for i in range(10)) ]
        self.size_picture = len(self.photosGaugeX220)
                              
        self.photoGaugeX220 = tkinter.PhotoImage(file=(os.path.join(self.path_aMagicEyes,'09.gif')))

        self.photoGauge = self.photoGaugeX220
        #print("jk-metermg: Photo width: {0}, height: {1}".format(self.photoGauge.width(),self.photoGauge.height()))
        #print("Photo width: %d, height: %d" % (self.photoGauge.width(),self.photoGauge.height()))

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
        #print ('layout --------------------')
        # set parameters that control the layout
        #self.configure(borderwidth=0,relief=SUNKEN)
        self.centrex = (int(self['width']))/2
        self.centrey = (int(self['height']))/2
        #print("jk-metermg: layout self.centrex: {0}, self.centrey: {1}".format(self.centrex,self.centrey))
        self.create_image(self.imageGauge.width/2,self.imageGauge.height/2,image=self.photoGauge)
        # standard with of lines
        self.linewidth = 2
        # outer radius for dial
        self.radius = int(0.40*float(self.centrex*2))
        #print ('jk-metermg: layout  self.radius: %s' % self.radius)
        # set width of bezel
        self.bezel = self.radius/15
        #print ('jk-metermg: layout  self.bezel: %s' % self.bezel)
        #self.bezelcolour1 = '#c0c0c0'
        self.bezelcolour1 = 'grey'
        #self.bezelcolour2 = '#808080'
        self.bezelcolour2 = 'green'
        # set lengths of ticks and hand
        self.majortick = self.radius/8
        self.minortick = self.majortick/2
        
        self.handlen = self.radius - self.majortick - self.bezel - 1
        #print ('jk-metermg: layout  self.handlen: %s' % self.handlen)
        self.blobrad = self.handlen/6
        #print ('jk-metermg: layout  self.blobrad: %s' % self.blobrad)
        self.configure(background='black')

    def graphics(self):
        #print ('jk-metermg: graphics --------------------')
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
        #print ('jk-metermg: setrange --------------------')
        self.start = start
        self.end = end
        self.range = end - start
        #print ("jk-metermg: setrange self.range: %s" % str(self.range))

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
        #print ('jk-metermg: blob --------------------')
        # call this to change the colour of the blob
        self.itemconfigure(self.blobid,fill = colour,outline = colour)
        parent_name = self.winfo_parent()
        #print ("jk-metermg: parent_name: %s" % str(parent_name))
        parent = self._nametowidget(parent_name)
        #print ("jk-metermg: parent: %s" % str(parent))

##        if 1 == 0:
##            self.apixel = self.imageGauge.getpixel( (self.imageGauge.width/2, self.imageGauge.height/2) )
##            self.red = self.apixel[0]
##            self.green = self.apixel[1]
##            self.blue = self.apixel[2]
##        else:
##            self.red,self.green,self.blue = self.imageGauge.getpixel( (self.imageGauge.width/2, self.imageGauge.height/2) )
##        print("jk-metermg: Red1: {0}, Green1: {1}, Blue1: {2}".format(self.red,self.green,self.blue))
##        self.handcolor = "#{0:02x}{1:02x}{2:02x}".format(self.clamp(self.red), self.clamp(self.green), self.clamp(self.blue))
##        print ('jk-metermg: createhand self.handcolor: %s' % str(self.handcolor))
    def clamp(self,x):
        return max(0, min(x, 255))        
    def getcenter(self):
        return self.handcenterx,self.handcentery
    def setcenter(self,x,y):
        self.handcenterx = x
        self.handcentery = y
        #print("jk-metermg: setcenter x: %d, y: %d" % (self.handcenterx,self.handcentery))
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
        #print(self.mousex,self.mousey)
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
