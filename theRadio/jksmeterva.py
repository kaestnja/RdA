#!/usr/bin/python3
version=160
modulname='jksmeterva'
#to better debug: on crash enter: import pdb; pdb.pm()
import sys,os #, socket, datetime, traceback
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

# class to show a gauge or panel meter
#class Clock(object):
class Meter(tkinter.Canvas):
    width = 0
    height = 0
    path_aGauge = os.path.join(sys.path[0],'aGauge')
    Background = os.path.join(os.path.join(sys.path[0],'aGauge'),'BellRoss1_X185_GaugeX210_SunscreenX220.png')
    linewidth = 2
    mousex = 0
    mousey = 0
    handcenterx = 0
    handcentery = 0
    handstartx = 0
    handstarty = 0
    handendx = 0
    handendy = 0
    handlinefill = 'white'
    handlinewidth = 2
    degstart = -60
    degend = 241
    minortickspace = 6
    majortickspace = 10
    inconfiguremode = 0
    storetextcolor = 'white'

    def __init__(self,master,*args,**kwargs):
        super(Meter,self).__init__(master,*args,**kwargs)
        self.width=int(self['width'])
        self.height=int(self['height'])
        print (modulname + ": self.width: %d, self.height: %d" % (self.width,self.height))
        typetxt = ''
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

        if (self.width==220 and self.height==220):
            self.layout()
            self.createhand()
            #self.setrange()
        self.bind("<Button 3>",self.configuremode)

    def setAttr(self,path):
        Meter.Background = path
        print (modulname + ": setAttr path: %s" % path)
        print (modulname + ": setAttr self.Background: %s" % self.Background)
        print (modulname + ": setAttr Meter.Background: %s" % self.Background)
    def getAttr(self):
        return Meter.Background

    def createtick(self,angle,length):
        # helper function to create one tick
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        radius = self.radius - self.bezel
        if modulname=='jksmeterva':
            self.handlinewidth = 1
            self.handlinefill = 'black'
        self.create_line(self.handcenterx - radius*cos,self.handcentery - radius*sin,self.handcenterx - (radius - length)*cos,self.handcentery - (radius - length)*sin,width = self.handlinewidth,fill = self.handlinefill)

    def layout(self):
        #self.configure(relief=SUNKEN)
        #self.configure(relief=RAISED)
        #self.configure(borderwidth=0,highlightthickness=0)
        self.width=int(self['width'])
        self.height=int(self['height'])
        print (modulname + ": self.width: %d, self.height: %d" % (self.width,self.height))
        
        self.imageGaugeX220 = PIL.Image.open(self.Background)
        self.imageGauge = self.imageGaugeX220
        #self.imageGauge = self.imageGaugeX220.resize((240, 320))
        #self.imageGauge = self.imageGaugeX220.rotate(90).resize((240, 320))
        #self.imageGauge = PIL.ImageDraw.Draw(self.imageGaugeX220)
        #/usr/bin/convert "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_Sunscreen.png" -resize "200x200!" -quality 100 "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_SunscreenX200.png"
        print (modulname + ": Image width: {0}, height: {1}".format(self.imageGauge.width,self.imageGauge.height))

        self.photoGaugeX220 = tkinter.PhotoImage(file=self.Background)
        self.photoGauge = self.photoGaugeX220
        #self.photoGauge = tkinter.PhotoImage(file="D://__Dropbox//Dropbox//aRadio//theRadio//aGauge//BellRoss1_X185_GaugeX210_SunscreenX220.png")
        #self.photoGauge = tkinter.PhotoImage(data=self.imageGaugeX220)
        #self.photoGauge = PIL.ImageTk.PhotoImage(self.imageGaugeX220)   #.convert('RGB') .convert('P')
        #self.photoGauge = tkinter.PhotoImage(self.imageGaugeX220)
        print (modulname + ": Photo width: {0}, height: {1}".format(self.photoGauge.width(),self.photoGauge.height()))
        #print (modulname + ":Photo width: %d, height: %d" % (self.photoGauge.width(),self.photoGauge.height()))

        #foreground='yellow'
        #self.create_image(20,20, anchor=NW, image=self.imageGauge)
        #self.create_image(int(self['height'])/2,100,image=self.imageGauge)
        # set parameters that control the layout
        #self.configure(borderwidth=0,relief=SUNKEN)
        self.centerx = round(int(self['width'])/2)
        self.centery = round(int(self['height'])/2)
        print (modulname + ": layout centerx: {0}, handcentery: {1}".format(self.centerx,self.centery))
        self.create_image(self.centerx,self.centery,image=self.photoGauge)
        
######## center hand position
        self.handcenterx = self.centerx 
        self.handcentery = self.centery
        if modulname=='jksmeterva':
            #self.handcentery = self.centery + round(int(self.centery)/2)
            self.handcentery = round(int(self.centery * 17/12))
        print (modulname + ": layout handcenterx: {0}, handcentery: {1}".format(self.handcenterx,self.handcentery))
######### outer radius for dial
        self.radius = int(round(0.40*float(self.handcentery*2)))
        if modulname=='jksmeterva':
            self.radius = round(int(self.centery))
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
        print (modulname + ": layout  self.majortick: %s" % self.majortick)
        self.minortick = int(round(self.majortick/2))
        print (modulname + ": layout  self.minortick: %s" % self.minortick)
        self.handlen = int(round(self.radius - self.majortick - self.bezel - 1))
        print (modulname + ": layout  self.handlen: %s" % self.handlen)
        self.blobrad = int(round(self.handlen/6))
        print (modulname + ": layout  self.blobrad: %s" % self.blobrad)
        self.configure(background='black')

######### create the static components
        print (modulname + ": graphics self.handcenterx: {0},- self.radius: {1}".format(self.handcenterx,self.radius))
        print (modulname + ": graphics self.handcentery: {0},- self.radius: {1}".format(self.handcentery,self.radius))
        print (modulname + ": graphics self.handcenterx: {0},+ self.radius: {1}".format(self.handcenterx,self.radius))
        print (modulname + ": graphics self.handcentery: {0},+ self.radius: {1}".format(self.handcentery,self.radius))
        if not modulname=='jksmeterva':
            self.create_oval(self.handcenterx-self.radius,self.handcentery-self.radius,self.handcenterx+self.radius,self.handcentery+self.radius,width = int(round(self.bezel/2)),outline = self.bezelcolour2, fill = 'black')
        if not modulname=='jksmeterva':
            self.create_oval(self.handcenterx-self.radius - self.bezel,self.handcentery-self.radius - self.bezel,self.handcenterx+self.radius + self.bezel,self.handcentery+self.radius + self.bezel,width = self.bezel,outline = self.bezelcolour1)#, fill = 'black')
        if not modulname=='jksmeterva':
            self.blobid = self.create_oval(self.handcenterx - self.blobrad,self.handcentery - self.blobrad,self.handcenterx + self.blobrad,self.handcentery + self.blobrad,outline = 'white', fill = 'green')
        # create text display
        if  modulname=='jksmeterva':
            self.textid = self.create_text(self.handcenterx,self.handcentery + 1*self.blobrad,fill = '#91732b',font = tkinter.font.Font(size = -int(self.majortick)),tags='valuetext',text='0')
            #self.texttypeid = self.create_text(self.centerx,self.centery * 27/32,fill = '#0d0d09',font = tkinter.font.Font(size = -int(self.majortick)),tags='valuetype',text='ms')
            #self.texttypeid = self.create_text(self.centerx,self.centery * 27/32,fill = '#0d0d09',font = tkinter.font.Font(size = -int(self.majortick)),tags='valuetype',text=typetxt)
        else:
            self.textid = self.create_text(self.handcenterx,self.handcentery + 5*self.blobrad,fill = 'white',font = tkinter.font.Font(size = -int(2*self.majortick)),tags='valuetext',text='0')


    def clamp(self,x):
        return max(0, min(x, 255))
    def createhand(self):
        # create moving and changeable bits
        self.handstartx = self.handcenterx
        self.handstarty = self.handcentery
        self.handendx   = self.handcenterx
        self.handendy   = self.handcentery - self.handlen
######## hand smooth
        self.handid = self.create_line(self.handstartx,self.handstarty,self.handendx,self.handendy
        ,width = 2*self.linewidth,activewidth = 4*self.linewidth
        #,smooth = True,stipple='gray75' #'gray75', 'gray50', 'gray25', 'gray12'
        ,fill = self.handlinefill,arrow='last') #,arrowshape(8,10,3)

    def setrange(self, start = 0, end = 100,typetxt='ms'):
        self.start = start
        self.range = end - start
        if  modulname=='jksmeterva':
            self.degstart = 50
            self.degend = 131
            self.minortickspace = 2
            self.majortickspace = 10
        else:
            self.degstart = -60
            self.degend = 241
            self.minortickspace = 6
            self.majortickspace = 30
        for deg in range(self.degstart,self.degend,self.minortickspace):
            self.createtick(deg,self.minortick) #angle,length
        for deg in range(self.degstart,self.degend,self.majortickspace):
            self.createtick(deg,self.majortick) #angle,length
        #print (modulname + ": setrange self.range: %s" % str(self.range))
        self.texttypeid = self.create_text(self.centerx,self.centery * 27/32,fill = '#0d0d09',font = tkinter.font.Font(size = -int(self.majortick)),tags='valuetype',text=typetxt)
      

    def set(self,value):
        if self.inconfiguremode == 0:
            self.itemconfigure(self.textid,text = str(value))
        #print (modulname + ":set value: %s" % str(value))
        # call this to set the hand  # convert value to range 0,100
        if  modulname=='jksmeterva':
            deg = 91*(value - self.start)/self.range - 135
        else:
            deg = 300*(value - self.start)/self.range - 240
        #print (modulname + ":set deg: %s" % str(deg))
        rad = math.radians(deg)
        #print (modulname + ":set rad: %s" % str(rad))
        #self.itemconfigure(self.textid,text = str(value))
        if  modulname=='jksmeterva':
            self.handstartx = self.handcenterx+(self.handlen/2)*math.cos(rad)
            self.handstarty = self.handcentery+(self.handlen/2)*math.sin(rad)
        else:
            self.handstartx = self.handcenterx + self.blobrad * math.cos(rad)
            self.handstarty = self.handcentery + self.blobrad * math.sin(rad)
        self.handendx   = self.handcenterx+self.handlen*math.cos(rad)
        self.handendy   = self.handcentery+self.handlen*math.sin(rad)
        if  modulname=='jksmeterva':
            if 1 == 0:
                self.apixel = self.imageGauge.getpixel( (self.handstartx, self.handstarty) )
                self.red = self.apixel[0]
                self.green = self.apixel[1]
                self.blue = self.apixel[2]
            else:
                self.red,self.green,self.blue = self.imageGauge.getpixel( (self.handstartx, self.handstarty) )
            #print (modulname + ": Red1: {0}, Green1: {1}, Blue1: {2}".format(self.red,self.green,self.blue))
            self.handlinefill = "#{0:02x}{1:02x}{2:02x}".format(self.clamp(self.red), self.clamp(self.green), self.clamp(self.blue))
        #print (modulname + ": createhand self.handlinefill: %s" % str(self.handlinefill))
        # reposition hand
        self.itemconfig(self.handid,fill=self.handlinefill)
        self.coords(self.handid,self.handstartx,self.handstarty,self.handendx,self.handendy)

    def blob(self,colour):
        # call this to change the colour of the blob
        self.itemconfigure(self.blobid,fill = colour,outline = colour)
        parent_name = self.winfo_parent()
        print (modulname + ": parent_name: %s" % str(parent_name))
        parent = self._nametowidget(parent_name)
        print (modulname + ": parent: %s" % str(parent))

    def getcenter(self):
        return self.handcenterx,self.handcentery
    def setcenter(self,x,y):
        self.handcenterx = x
        self.handcentery = y
        print (modulname + ": setcenter x: %d, y: %d" % (self.handcenterx,self.handcentery))
        print (modulname + ": setcenter backgroundpicpath: %s" % self.backgroundpicpath)

    def configuremode(self,eventorigin):
        #tag='valuetext'  #textid
        print (modulname + ": inconfiguremode: %s" % str(self.inconfiguremode))
        if self.inconfiguremode == 0:
            self.storetextcolor=self.itemcget(self.textid, "fill")
            self.itemconfig(self.textid,fill = 'red')
            self.inconfiguremode = 1
            self.bind("<Button 1>",self.getorigin)
        else:
            self.itemconfig(self.textid,fill = self.storetextcolor)
            self.inconfiguremode = 0
            self.unbind("<Button 1>")

    def getorigin(self,eventorigin):
        self.mousex = eventorigin.x
        self.mousey = eventorigin.y
        print (self.mousex,self.mousey)
        self.itemconfigure( self.textid,text = str(self.mousex) + ' ' + str(self.mousey)   )
        self.red,self.green,self.blue = self.imageGauge.getpixel( (self.mousex, self.mousey))
        print (modulname + ": Red1: {0}, Green1: {1}, Blue1: {2}".format(self.red,self.green,self.blue))
        print (modulname + "#{0:02x}{1:02x}{2:02x}".format(self.clamp(self.red), self.clamp(self.green), self.clamp(self.blue)))
        #self.handlinefill = "#{0:02x}{1:02x}{2:02x}".format(self.clamp(self.red), self.clamp(self.green), self.clamp(self.blue))


if __name__ == '__main__':
    print (modulname + ": in main")
    root.mainloop()
    exitfunc()
    #root.destroy()
