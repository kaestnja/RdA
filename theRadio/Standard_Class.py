#!/usr/bin/python3
"""
Sample Classes
Holds the Sample Classes (base and inherited).
Some Informative Notes Goes Here ...
 Revision: 1.0 $Date: 24/07/2007 21:00$
History
 v. 1.0 - Initial Class Creation
 v. 1.1 - ...
 """
__version__ = '$Revision: $'
"""
 To Do:
 -https://docs.microsoft.com/de-de/visualstudio/python/debugging-python-code-on-remote-linux-machines
 -https://pythonprogramming.net/object-oriented-programming-crash-course-tkinter/
 -https://stackoverflow.com/questions/29497391/creating-a-tkinter-class-and-waiting-for-a-return-value
 -https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
 -http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
"""
remotedebugg = 0
if remotedebugg:
    import ptvsd #pip3 install ptvsd
    #ptvsd.enable_attach('my_secret') #tcp://my_secret@192.168.178.29:5678
    ptvsd.enable_attach(secret = 'my_secret', address = ('0.0.0.0', 8080))
    #ptvsd.enable_attach(secret=None)
    ptvsd.wait_for_attach
# =============================================================================
# Standard Python modules
# =============================================================================
import os, sys, math, string, struct, socket, time, datetime, traceback, subprocess, pathlib
import ftplib, contextlib, shutil
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
import tkinter
from tkinter import font, ttk, colorchooser
#from tkinter import *       #tkinter.Button
#available in ttk: Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, PanedWindow, Radiobutton, Scale, Scrollbar
#from tkinter.ttk import *  tkinter.ttk.Button
# =============================================================================
# External Python modules
import pip
def install(package):
    pip.main(['install', package])
# =============================================================================
import numpy, psutil, pysftp, requests, timeit, platform, multiprocessing, threading
import PIL  #pip3 install pillow  or  python -m pip install pillow or sudo apt-get install python3-pil.imagetk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import urllib
import urllib.parse    #from urllib.parse import urlsplit, urlunsplit
import urllib.request
#from urllib.parse import urlsplit, urlunsplit
#import urllib.parse  #from urllib import request, parse  #from urllib.parse import urlsplit, urlunsplit #import urllib.request
try:
    import RPi.GPIO
    gpio_exist=1
except:
    print ("jk-import RPi.GPIO failed")
    traceback.print_exc()
try:
    import win32com.client as wincl
    wincl.Dispatch("SAPI.SpVoice").Speak("Hallo Lisa")
    mp = wincl.Dispatch("WMPlayer.OCX")
except:
    traceback.print_exc()
    #install("pypiwin32") # also tried 'pywin32'
    #import win32com #pip install pywin32 didn't work for me but pypiwin32 did
# =============================================================================
# Extension modules
# =============================================================================
#import extension

# =============================================================================
# Misc Definitions
# =============================================================================

# =============================================================================
# First Class
# =============================================================================
class Sample_Class(object):
    """
     Sample Class
    """

    def __init__(self, assign_input={}, *optional_value_input, **optional_dict_input):
        """
        Sample Class Initialization

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

        # Default Values

        # Input Checks

        # init ...
        self.attribute = assign_input

    def __Private_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

    def Public_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

# =============================================================================
# Second Class
# =============================================================================
class Inherited_Class(Sample_Class):

    """
    Sample Class
    """

    def __init__(self, assign_input={}, *optional_value_input, **optional_dict_input):
        """
        Sample Class Initialization

        Keyword Arguments:
        ------------------
        self. -> STRING: Description. Default = 

        Input Attributes:
        -----------------
        self. -> SCALAR: Description. Default = 

        Additional Attributes:
        ----------------------
        self. -> SCALAR: Description. Default = 

        Documentation last updated: Month. Day, Year - Author
        """

        # Default Values

        # Input Checks

        # init ...
        self = Sample_Class(assign_input={}, *optional_value_input, **optional_dict_input)
        self.inherited_exclusive_attribute = "from some input ..."

    def __Private_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

    def Public_Method(self):

        """
        Private Module
        """

        # Inputs

        # Module Code

        # Output

    # =============================================================================
    # Private Functions
    # =============================================================================
    def __Private_Function(inputs):

        """
        Private Function
        """

        # Inputs

        # Function code ...

    # =============================================================================
    # Public Function
    # =============================================================================
    def Public_Function(inputs):

        """
        Public Function
        """

        # Inputs

        # Function code ...

    # =============================================================================
    # Private Functions
    # =============================================================================
    def __Private_Function(self):

        """
        Function
        """

        # Function code ...

        return outputs

    # =============================================================================
    # Public Functions
    # =============================================================================
    def Public_Function(self):

        """
        Function
        """

        # Function code ...

        return outputs

#==============================================================================
# Class Test
#==============================================================================
if __name__ == '__main__':

    # Test Parent
    parent = Sample_Class()
    parent.Public_Method()

    # Test Child
    child = Inherited_Class()
    child.Public_Method()
