#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tkinter
import math
import os
import sys

class Meter(tkinter.Frame):
    def __init__(self, master=None, **kw):
        tkinter.Frame.__init__(self, master, **kw)

        self.meter = []
        self.angle = []
        self.var = tkinter.IntVar(self, 0)

        self.path_script = sys.path[0]
        self.imageGaugeTemp = tkinter.PhotoImage(file=os.path.join(self.path_script + '//aGauge','GaugeX200.png')) #Default - Kopie.png
        
        #https://www.daniweb.com/programming/software-development/threads/453249/setting-an-image-as-a-background
        #bg_image = tk.PhotoImage(file=fname)
        # get the width and height of the image
        #w = bg_image.width()
        #h = bg_image.height()
        
        
        self.canvas = tkinter.Canvas(self, width=200, height=210, borderwidth=2, relief='sunken', bg='white')
        #self.image_on_canvas = self.canvas.create_image(0, 0, anchor = tkinter.NW, image = self.imageGaugeTemp)  #anchor = tkinter.NW,
        self.scale = tkinter.Scale(self, orient='horizontal', from_=0, to=100, variable=self.var)

        for j, i in enumerate(range(0, 100, 5)):
            print ("i=%s" % str(i))
            print ("j=%s" % str(j))
            self.meter.append(self.canvas.create_line(100, 100, 10, 100, activefill='red', fill='grey%i' % i, width=3, arrow='last'))
            self.angle.append(0)
            self.canvas.lower(self.meter[j])
            self.updateMeterLine(0.2, j)

        self.canvas.create_arc(10, 10, 190, 190, extent=108, start=36, style='arc', outline='red')
        self.canvas.pack()
        #self.canvas.pack(fill='both')
        self.scale.pack()
        print (self.canvas.find_above(self.imageGaugeTemp ))
        ##########################################################################
        #self.canvas.itemconfig(self.image_on_canvas, bg = self.imageGaugeTemp)
        ##########################################################################
        try:
            print ("before trace_add")
            self.var.trace_add('write', self.updateMeter)  # if this line raises an error, change it to the old way of adding a trace: self.var.trace('w', self.updateMeter)
            print ("after trace_add")
        except AttributeError:
            print ("except trace_add")
            self.var.trace('w', self.updateMeter)
            pass
            
        self.updateMeterTimer()

    def updateMeterLine(self, a, l=0):
        """Draw a meter line (and recurse for lighter ones...)"""
        oldangle = self.angle[l]
        self.angle[l] = a
        x = 100 - 90 * math.cos(a * math.pi)
        y = 100 - 90 * math.sin(a * math.pi)
        self.canvas.coords(self.meter[l], 100, 100, x, y)
        l += 1
        if l < len(self.meter):
            self.updateMeterLine(oldangle, l)

    def updateMeter(self, name1, name2, op):
        """Convert variable to angle on trace"""
        mini = self.scale.cget('from')
        maxi = self.scale.cget('to')
        pos = (self.var.get() - mini) / (maxi - mini)
        self.updateMeterLine(pos * 0.6 + 0.2)

    def updateMeterTimer(self):
        """Fade over time"""
        self.var.set(self.var.get())
        self.after(2, self.updateMeterTimer)


if __name__ == '__main__':
    root = tkinter.Tk()
    meter = Meter(root)
    meter.pack()
    root.mainloop()
