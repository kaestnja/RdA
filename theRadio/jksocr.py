#!/usr/bin/python3
version=160
modulname='jk-nixieclock'
#to better debug: on crash enter: import pdb; pdb.pm()
#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
#https://www.python-course.eu/python3_class_and_instance_attributes.php
import sys,os, socket, datetime, traceback, math, time
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
########################################################################################
import tkinter
from tkinter import font, ttk, colorchooser
import PIL  #pip3 install pillow  or  python -m pip install pillow or sudo apt-get install python3-pil.imagetk
from PIL import Image, ImageTk, ImageDraw, ImageFont

global tesserocr_use
tesserocr_use = 0
if ocr_use == 1:
    global ocr_exist
    ocr_exist = 0
    try:
        import tesserocr
        ocr_exist=1
        #import tesserocr #sudo apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev
        #pip3 install --upgrade tesserocr
        #pip3 install --upgrade pip
        #pip3 install --upgrade D:\Downloads\tesserocr-2.2.2-cp36-cp36m-win32.whl
        # cd C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_86
        # python -m pip install  --upgrade D:\Downloads\tesserocr-2.2.2-cp36-cp36m-win32.whl
        # cd C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64
        #python -m pip install --upgrade tesserocr tesseract-ocr 
        #python -m pip install --upgrade pip
        #https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/
    except:
        print ("jk-import tesserocr failed")
        traceback.print_exc()
global pyocr_use
pyocr_use = 0
if pyocr_use == 1:
    try:
        import pyocr #pip3 install --upgrade pyocr
        import pyocr.builders
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
        else:
            #https://github.com/openpaperwork/pyocr
            tool = tools[0]
            print("Will use tool '%s'" % (tool.get_name()))
            langs = tool.get_available_languages()
            print("Available languages: %s" % ", ".join(langs))
            lang = langs[0]
            print("Will use lang '%s'" % (lang))
            ocr_exist=1
    except:
        print ("jk-import pyocr failed")
        traceback.print_exc()

global pytesseract_use
pytesseract_use = 0
if pytesseract_use == 1:
    try:
        import cv2 #pip3 install --upgrade opencv-python #python -m pip install --upgrade opencv-python
        import argparse #pip3 install --upgrade argparse #python -m pip install --upgrade argparse
        import pytesseract #pip3 install --upgrade pytesseract #python -m pip install --upgrade pytesseract
    except:
        print ("jk-import pytesseract failed")
        traceback.print_exc()
###########################################################################
#from tkinter import *       #tkinter.Button
#available in ttk: Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar
#from tkinter.ttk import *  tkinter.ttk.Button

#/usr/bin/convert "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_Sunscreen.png" -resize "200x200!" -quality 100 "/home/pi/aRadio/theRadio/aGauge/BellRoss1_X185_GaugeX210_SunscreenX200.png"
#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
#class Clock(object):
class JKOCR(tkinter.Canvas):
    width = 0
    height = 0
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

        if ocr_use == 1 and ocr_exist == 1:
            #https://pypi.python.org/pypi/tesserocr
            try:
                print ("tesseract_version: %s" %  str(tesserocr.tesseract_version()))
                for file in os.listdir(str(self.NumberPicFolderPath)):
                    #image = PIL.Image.open(file)
                    print ("file: %s" % str(os.path.join(self.NumberPicFolderPath,file)))
                    image = PIL.Image.open(os.path.join(self.NumberPicFolderPath,file))
                    print ("identified text1: %s" % str(tesserocr.image_to_text(image)))  # print ocr text from image
                    print ("identified text2: %s" % str(tesserocr.file_to_text(os.path.join(self.NumberPicFolderPath,file))))
            except:
                print ("jk-import pytesseract failed later")
                traceback.print_exc()
 
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
 
    def clamp(self,x):
        return max(0, min(x, 255))

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
    root.mainloop()
    root.quit()
