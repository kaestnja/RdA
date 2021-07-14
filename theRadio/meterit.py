#!/usr/bin/python3
import sys, os, socket, datetime
import inspect, math
import tkinter
from tkinter import font, ttk, colorchooser
#from tkinter import *       #tkinter.Button
#available in ttk: Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar
#from tkinter.ttk import *  tkinter.ttk.Button
#pip3 install pillow  or  python -m pip install pillow
import PIL
from PIL import Image, ImageTk
import jksmeter360 as meter360
import jksmeterva as meterva
import jksmetermg as metermg
import jksnixieclock as nixieclock
#global squareOf
#global startOf
#global endOf
#global valueOf
squareOf=220
startOf=0
endOf=100
valueOf=(endOf-startOf)/2
noborder=0
#global the_hostname
the_hostname = socket.gethostname()

#style = ttk.Style()
#style.configure("BW.TLabel", foreground="black", background="white")
#style.configure("WB.TLabel", foreground="white", background="white")

#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
class MeterMGMainframe(tkinter.Frame):

    def __init__(self,master,*args,**kwargs):
        super(MeterMGMainframe,self).__init__(master,*args,**kwargs)
        if noborder == 1:
            self.configure(borderwidth=0,highlightthickness=0)
        self.path_script = sys.path[0]
        self.path_aMagicEye = os.path.join(self.path_script,'aMagicEye')
        self.path_aMagicEyes = os.path.join(self.path_aMagicEye,'BellRoss1_X185_GaugeX210_SunscreenX220_1-10_gif')
        self.metermg = metermg.Meter(self,height = squareOf,width = squareOf)
        self.metermg.pack()

        if hasattr(self.metermg, 'setcenter'):
            setattr(self.metermg, 'setcenter', (50,50))
        if hasattr(self.metermg, 'getcenter'):
            print("MeterMGMainframe get X: %d, Y: %d" % (self.metermg.getcenter()))

        if noborder == 1:
            self.metermg.configure(borderwidth=0,highlightthickness=0)
        self.metermg.setrange(startOf,endOf)

        #self.metermg.set(valueOf)
        self.metervascale = tkinter.Scale(self, from_ = startOf, to = endOf, orient = tkinter.HORIZONTAL, command = self.setmeter).pack()
        self.metervabutton50 = tkinter.ttk.Button(self, text = "50", width = 15, command = lambda: self.callback(50)).pack()
        self.metervacheckbuttonPos = tkinter.Checkbutton(self,relief=tkinter.RAISED, text = "Pos", width = 15, command = lambda: self.getmetersettings(),indicatoron=0).pack() #Radiobutton,Checkbutton
        self.metervabuttonselectcolor = tkinter.Button(self,relief=tkinter.RAISED, text = 'Select Color', width = 15,command = lambda: self.getColor()).pack()
        #self.metermg.blob('yellow')

    def getColor(self):
        color = askcolor()
        print ("MeterMGMainframe  getColor: %s" % str(color))

    def callback(self,value):
        self.metermg.set(value)

    def setmeter(self,value):
        #print (value)
        value = int(value)
        valueOf = value
        self.metermg.set(value)

    def getmetersettings(self):
        print("MeterMGMainframe getmetersettings X: %d, Y: %d" % (self.metermg.getcenter()))
#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
class MeterVAMainframe(tkinter.Frame):

    def __init__(self,master,*args,**kwargs):
        super(MeterVAMainframe,self).__init__(master,*args,**kwargs)
        #self.pack()
        if noborder == 1:
            self.configure(borderwidth=0,highlightthickness=0)
        #self.metervaframe = tkinter.Frame(self
                                          #,relief=RAISED
                                     #,borderwidth=0,highlightthickness=0
                                     #,background='black'
                                     ##,activebackground='black'
                                     ##,foreground='black'
                                     #,highlightbackground='black'
                                     #,highlightcolor='black'
                                     ##,troughcolor='black'
                                     #,style="BW.TLabel"
                                     #)
        #self.metervaframe.pack()
        #if noborder == 1:
            #self.metervaframe.configure(borderwidth=0,highlightthickness=0)
        #self.metervaimagelabel = tkinter.Label(self.metervaframe)
        #self.metervaimagelabel.pack()
        #if noborder == 1:
            #self.metervaimagelabel.configure(borderwidth=0,highlightthickness=0)
##        #self.meter = meterva.Meter(self,height = squareOf,width = squareOf)
        #self.meterva = meterva.Meter(self.metervaimagelabel,height = squareOf,width = squareOf)
        #self.meterva = meterva.Meter(self,height = squareOf,width = squareOf,centerx = 0, centery = 0)
        self.meterva = meterva.Meter(self,height = squareOf,width = squareOf)

        #self.meterva.Background = 'test2'
        print("MeterVAMainframe getattr0 Background: %s" % (getattr(self.meterva, 'Background')))

        if hasattr(self.meterva, 'Background'):
            setattr(self.meterva, 'Background', 'test1')
            print("MeterVAMainframe getattr1 Background: %s" % (getattr(self.meterva, 'Background')))

        setattr(self.meterva, 'Background', 'test2')

        if hasattr(self.meterva, 'Background'):
            print("MeterVAMainframe getattr2 Background: %s" % (getattr(self.meterva, 'Background')))

########
        print("MeterVAMainframe getattr3 Background: %s" % (self.meterva.getAttr()))

        if hasattr(self.meterva, 'Background'):
            setattr(self.meterva, 'Background', 'test3')

        self.meterva.setAttr('Background=test4')

        if hasattr(self.meterva, 'Background'):
            print("MeterVAMainframe getattr4 Background: %s" % (self.meterva.getAttr()))


        if hasattr(self.meterva, 'setcenter'):
            setattr(self.meterva, 'setcenter', (50,50))
        if hasattr(self.meterva, 'getcenter'):
            print("MeterVAMainframe get X: %d, Y: %d" % (self.meterva.getcenter()))
        self.meterva.pack()

        if noborder == 1:
            self.meterva.configure(borderwidth=0,highlightthickness=0)
##        #self.meter.setrange(20,90)
        self.meterva.setrange(startOf,endOf)

        #self.meterva.set(valueOf)  imageNixieBack440X220 ClockBackgroundPicPath
        #tkinter.Scale(self,width = 15 ,from_ = 20, to = 90 ,orient = HORIZONTAL,command = self.setmeter).pack()
        #tkinter.Scale(self, width = 15, from_ = startOf, to = endOf, orient = HORIZONTAL, command = self.setmeter).pack()
        self.metervascale = tkinter.Scale(self, from_ = startOf, to = endOf, orient = tkinter.HORIZONTAL, command = self.setmeter).pack()
        self.metervabutton50 = tkinter.ttk.Button(self, text = "50", width = 15, command = lambda: self.callback(50)).pack()
        self.metervacheckbuttonPos = tkinter.Checkbutton(self,relief=tkinter.RAISED, text = "Pos", width = 15, command = lambda: self.getmetersettings(),indicatoron=0).pack() #Radiobutton,Checkbutton
        self.metervabuttonselectcolor = tkinter.Button(self,relief=tkinter.RAISED, text = 'Select Color', width = 15,command = lambda: self.getColor()).pack()
        #self.meter.blob('yellow')
        #self.itemconfigure(fill = 'yellow')#,outline = colour)

    def getColor(self):
        color = askcolor()
        print ("MeterVAMainframe  getColor: %s" % str(color))

    def callback(self,value):
        self.meterva.set(value)

    def setmeter(self,value):
        #print (value)
        value = int(value)
        valueOf = value
        self.meterva.set(value)

    def getmetersettings(self):
        print("MeterVAMainframe getmetersettings X: %d, Y: %d" % (self.meterva.getcenter()))

class Meter360Mainframe(tkinter.Frame):
    Meter360MainframeValue = 0
    def __init__(self,master,*args,**kwargs):
        super(Meter360Mainframe,self).__init__(master,*args,**kwargs)
        #self.pack()
        if noborder == 1:
            self.configure(borderwidth=0,highlightthickness=0)
        self.meter360 = meter360.Meter(self,height = squareOf,width = squareOf)
        self.meter360.pack()
        if noborder == 1:
            self.meter360.configure(borderwidth=0,highlightthickness=0)
##        #self.meter.setrange(20,90)
        self.meter360.setrange(startOf,endOf)
        self.meter360.set(valueOf)
        #tkinter.Scale(self, width = 15, from_ = startOf, to = endOf, orient = HORIZONTAL, command = self.setmeter).pack()
        self.meterscale = tkinter.Scale(self, from_ = startOf, to = endOf, orient = tkinter.HORIZONTAL, command = self.setmeter, digits=0).pack()
        self.meterbuttonquit = tkinter.ttk.Button(self, text = 'Quit', width = 15, command = master.destroy).pack()
        self.meterbutton50 = tkinter.Button(self, text = "50", width = 15, command = lambda: self.callback(50)).pack()
        self.metercheckbuttonselectcolor = tkinter.Checkbutton(self, text = 'Select Color', width = 15,command = lambda: self.getColor(),indicatoron=0).pack() #Radiobutton,Checkbutton
        #self.meter.blob('yellow')
        #self.itemconfigure(fill = 'yellow')#,outline = colour)

    def getColor(self):
        color = askcolor()
        print ("jk-meterit Meter360Mainframe color: %s" % str(color))

    def callback(self,value):
        self.meter360.set(value)

    def setmeter(self,value):
        #print (value)
        value = int(value)
        self.Meter360MainframeValue = value
        self.meter360.set(value)

class NixieClockMainframe(tkinter.Frame):
    NixieClockMainframeValue = 0
    def __init__(self,master,*args,**kwargs):
        super(NixieClockMainframe,self).__init__(master,*args,**kwargs)
        #self.pack()
        if noborder == 1:
            self.configure(borderwidth=0,highlightthickness=0)
        self.nixieclock = nixieclock.Clock(self,height = 120,width = 440)
        self.nixieclock.pack()
        if noborder == 1:
            self.nixieclock.configure(borderwidth=0,highlightthickness=0)
        self.nixieclock.set(0)
        self.nixieclock.configure(height = 220,width = 440)
        self.nixieclock.configure(borderwidth=1,highlightthickness=0)
        self.nixieclock.configure(background='orange')

        if 0 == 1:
            self.ClockMainframeBackgroundPicPath = os.path.join(os.path.join(os.path.join(os.path.join(sys.path[0],'aNixie'),'nixie_digits_1_0_by_jrandomnoob-d9i6tss'),'png')
                                                                ,'background_440x220.png')
            self.nixieclock.setClockBackgroundPicPath( path=self.ClockMainframeBackgroundPicPath )
        print ("jk-NixieClockMainframe: getClockBackgroundPicPath: %s" % str(self.nixieclock.getClockBackgroundPicPath()))
        if 0 == 1:
            #self.ClockMainframeNumberPicFolderPath = os.path.join(os.path.join(os.path.join(sys.path[0],'aNixie'),'nixie_digits_1_0_by_jrandomnoob-d9i6tss'),'png')
            self.ClockMainframeNumberPicFolderPath = os.path.join(os.path.join(os.path.join(sys.path[0],'aNixie'),'nixie_tube_numbers__resource__by_nickpolyarush'),'png')
            #self.ClockMainframeNumberPicFolderPath = os.path.join(os.path.join(os.path.join(sys.path[0],'aNixie'),'nixie_tube_numbers__resource__by_nickpolyarush'),'png')
            self.nixieclock.setNumberPicFolderPath( path=self.ClockMainframeNumberPicFolderPath,size='90x140' )
        print ("jk-NixieClockMainframe: getNumberPicFolderPath   : %s" % str(self.nixieclock.getNumberPicFolderPath()))
        #tkinter.Scale(self, width = 15, from_ = startOf, to = endOf, orient = HORIZONTAL, command = self.setmeter).pack()
        self.meterscale = tkinter.Scale(self, from_ = 0, to = (60*60*24)-1, orient = tkinter.HORIZONTAL, command = self.setclockseconds, digits=0).pack()
        self.meterbuttonquit = tkinter.ttk.Button(self, text = 'Quit', width = 15, command = master.destroy).pack()
        self.meterbutton50 = tkinter.Button(self, text = "20050", width = 15, command = lambda: self.setclockseconds(20050)).pack()
        self.clockbutton = tkinter.Button(self, text = "23,59,59", width = 15, command = lambda: self.setclockdaytime(12,59,59)).pack()
        self.clockcheckbutton = tkinter.Checkbutton(self, text = '2,9,5', width = 15,command = lambda: self.setclockdaytime(2,9,5),indicatoron=0).pack() #Radiobutton,Checkbutton
        #self.meter.blob('yellow')
        #self.itemconfigure(fill = 'yellow')#,outline = colour)
    def setclockseconds(self,value):
        #self.nixieclock.set(value)
        m, s = divmod(int(value), 60)
        h, m = divmod(m, 60)
        self.setclockdaytime(h, m, s)
    def setclockdaytime(self,h,m,s):
        print ("%d:%02d:%02d" % (h, m, s))
        self.nixieclock.set_Clock(h,m,s)

    def setmeter(self,value):
        #print (value)
        value = int(value)
        self.NixieClockMainframeValue = value
        self.nixieclock.set(value)
        


class App(tkinter.Tk):
    def __init__(self):
        super(App,self).__init__()
        self.width = 600
        self.height = 400
        self.lefttopx = 0
        self.lefttopy = 0
        ####################################################################
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        if  'test51' in the_hostname:
            self.lefttopy = screen_height - self.height - 100
        else:
            self.lefttopy = screen_height - self.height - 40 - 40
        print("jk-screen width:%d height:%d" % (screen_width,screen_height))
        if self.width > screen_width:
            self.width = screen_width
        if self.height > screen_height:
            self.height = screen_height
        self.geometry("%dx%d+%d+%d" % (self.width, self.height, self.lefttopx, self.lefttopy)) #screen_height))
        #self.create_image(20,20, anchor=NW, image=self.imageGaugeTemp)
        self.configure(background='black')
##        IconFile = os.path.join( program_directory ) + "\ApplicationIcon.gif"
##        IconImage = PhotoImage( file = IconFile )
##        self.tkinter.call( 'wm', 'iconphoto', root._w, IconImage )
        self.title('Try Meter')
        if noborder == 1:
            self.configure(borderwidth=0,highlightthickness=0)
        #NixieClockMainframe(self).pack(side=tkinter.TOP)
        Meter360Mainframe(self).pack(side=tkinter.LEFT)
        MeterMGMainframe(self).pack(side=tkinter.LEFT)
        MeterVAMainframe(self).pack(side=tkinter.LEFT)
        

        #tkinter.Scale(self, width = 15, from_ = startOf, to = endOf, orient = HORIZONTAL, command = self.setmeter).pack()
        #self.meterscale = tkinter.Scale(self, from_ = startOf, to = endOf, orient = tkinter.HORIZONTAL, command = Meter360Mainframe.setmeter(self), digits=0).pack(side=tkinter.BOTTOM)


App().mainloop()
