#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 22:27:55 2018

@author: Jan
"""

# clock_ex3.py

# a pygtk widget that implements a clock face
# porting of Davyd Madeley's 
# http://www.gnome.org/~davyd/gnome-journal-cairo-article/clock-ex3.c

# author: Lawrence Oluyede <l.oluyede@gmail.com>
# date: 03 December 2005

#import gtk

#https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html#simple-example
#import gi
#gi.require_version('Gtk', '3.0')
#from gi.repository import Gtk as gtk

import string
import os
import gi
import cairo
import math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, Gdk



#In Gtk+ v3 the expose_event is now called 'draw', so change this line:
#-     drawing_area.connect('expose-event',self.expose)
#with:
#+     drawing_area.connect('draw',self.expose)

class EggClockFace(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        window = gtk.Window()
        window.connect("destroy", gtk.main_quit)
        #self.connect("expose_event", self.expose)
        self.connect('draw', self.expose)
        
    def expose(self, widget, event):
        self.context = widget.window.cairo_create()
        
        # set a clip region for the expose event
        self.context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        self.context.clip()
        
        self.draw(self.context)
        
        return False
    
    def draw(self, context):
        rect = self.get_allocation()
        x = rect.x + rect.width / 2
        y = rect.y + rect.height / 2
        
        radius = min(rect.width / 2, rect.height / 2) - 5
        
        # clock back
        context.arc(x, y, radius, 0, 2 * math.pi)
        context.set_source_rgb(1, 1, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.stroke()
        
        # clock ticks
        for i in xrange(12):
            context.save()
            
            if i % 3 == 0:
                inset = 0.2 * radius
            else:
                inset = 0.1 * radius
                context.set_line_width(0.5 * context.get_line_width())
            
            context.move_to(x + (radius - inset) * math.cos(i * math.pi / 6),
                            y + (radius - inset) * math.sin(i * math.pi / 6))
            context.line_to(x + radius * math.cos(i * math.pi / 6),
                            y + radius * math.sin(i * math.pi / 6))
            context.stroke()
            context.restore()
        

def main():
    window = gtk.Window()
    clock = EggClockFace()
    
    window.add(clock)
    window.connect("destroy", gtk.main_quit)
    window.show_all()
    
    gtk.main()
    
if __name__ == "__main__":
    main()
