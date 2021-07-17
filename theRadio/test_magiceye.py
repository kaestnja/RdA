#!/usr/bin/python3
version=131
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
#is_py2 = sys.version[0] == '2'
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
    quit()
########################################################################################
import tkinter #from tkinter import *
import tkinter.font
import math

if __name__ == '__main__':
    root = tkinter.Tk()

global path_script
path_script = sys.path[0]

root.configure(background='black')
root.title("path: %s" % str(path_script))

rightframe = tkinter.Frame(root,width=155, borderwidth=1, relief=tkinter.SUNKEN,background='black')
rightframe.pack(side=tkinter.RIGHT,fill=tkinter.Y)

imagesMagicEye = [tkinter.PhotoImage(file=os.path.join(path_script + '//aMagicEye','6ZE11Resized200__1-10.gif'), format = 'gif -index %i' %(i)) for i in range(10)]
imageGaugeTemp = tkinter.PhotoImage(file=os.path.join(path_script + '//aGauge','GaugeX200.png'))

root.imagesMagicEye = imagesMagicEye
root.imageGaugeTemp = imageGaugeTemp

imagelabel = tkinter.Label(rightframe)
imagelabel.pack()
imagelabel.configure(image=imagesMagicEye[0])
picture_old = 0
picture_current = len(imagesMagicEye)-1
direction_steps = 1

def change_pictures():
    for i in range(picture_old,picture_current,direction_steps):
        print (i)
        time.sleep(2)
        imagelabel.configure(image=imagesMagicEye[i])
def set_picture(value):
    print (value)
    value=int(value)
    imagelabel.configure(image=imagesMagicEye[value])

test0 = tkinter.Scale(rightframe, width = 15, from_ = 0, to = len(imagesMagicEye)-1, orient = tkinter.HORIZONTAL, command = set_picture, digits=0).pack()
root.mainloop()
