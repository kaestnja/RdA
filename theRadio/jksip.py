#!/usr/bin/python3
version=155
modulname='jksip'

#https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
#https://www.python-course.eu/python3_class_and_instance_attributes.php
#to better debug: on crash enter: import pdb; pdb.pm()
import sys,os, socket, datetime, traceback
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
import struct, subprocess, multiprocessing, threading
##################################
import requests as requests
import urllib
from urllib import request, parse
#import urllib.parse
#from urllib.parse import urlsplit, urlunsplit
##################################
class JKSIP:
    ip_internal = ''
    ip_gateway = ''
    ip_host = ''
    counter = 0
    class_attribute = 'version=155'
    Background = 'empty'

    #def __init__(self,master,*args,**kwargs):
    def __init__(self,instance_attribute,*args,**kwargs):
        type(self).counter += 1
        self.instance_attribute = instance_attribute
##        #https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide
##        foo = MyClass(2)
##        bar = MyClass(3)
##        foo.class_attribute, foo.instance_attribute
##        ## version=144, 2
##        bar.class_attribute, bar.instance_attribute
##        ## version=144, 3
##        MyClass.class_attribute ## <— This is key
##        ## version=144

        #super(JKSIP,self).__init__(master,*args,**kwargs)
        super(JKSIP,self).__init__(*args,**kwargs)
##        print("jk-meterva: self.width: %d, self.height: %d" % (self.width,self.height))
##        self.width=int(self['width'])
##        self.height=int(self['height'])
##        print("jk-meterva: self.width: %d, self.height: %d" % (self.width,self.height))
        #if self is not None:
            #print (modulname + " self: %s" % str(self))    #.!metervamainframe.!meter
        if args is not None:
            for value in args:
                print (modulname + " arg: %s" % str(value))
        if kwargs is not None:
            for key, value in kwargs.items():
                print (modulname + " kwarg: %s == %s" %(key,value))
        #print("jk-meterva: Image width: {0}, height: {1}".format(self.imageGauge.width,self.imageGauge.height))
        #print("jk-meterva: Photo width: {0}, height: {1}".format(self.photoGauge.width(),self.photoGauge.height()))
        #print("Photo width: %d, height: %d" % (self.photoGauge.width(),self.photoGauge.height()))

    def __del__(self):
        type(self).counter -= 1

    def setAttr(self,path):
        JKSIP.Background = path
        print (modulname + ": setAttr path: %s" % path)
        print (modulname + ": setAttr self.Background: %s" % self.Background)
        print (modulname + ": setAttr JKSIP.Background: %s" % JKSIP.Background)
    def getAttr(self):
        return JKSIP.Background
    ################################################################################################################
    def get_ip_internal(self):
        ip_myself = self.get_local_ip()
        self.ip_internal = str(ip_myself)
        return self.ip_internal

    def get_local_ip(self):
        """ Tries to determine the local IP address of the machine. """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Use Google Public DNS server to determine own IP
            sock.connect(('8.8.8.8', 80))
            ip_addr = sock.getsockname()[0]
            sock.close()
            print(modulname + " get_local_ip via 8.8.8.8  ---: %s" % str(ip_addr))
            return ip_addr
        except socket.error:
            traceback.print_exc()
            print (modulname + " get_local_ip via gethostbyname")
            return socket.gethostbyname(socket.gethostname())

    def get_ip_gateway(self):
        if sys.platform == "win32":
            self.ip_gateway = self.get_default_gateway_windows()
        else:
            self.ip_gateway = self.get_default_gateway_linux()
        return self.ip_gateway

    def get_default_gateway_linux(self): # import socket;import struct
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue
                #self.ip_gateway = str(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))
                #print("jk-JKSIP: get_default_gateway_linux ip_gateway: %s" % self.ip_gateway)
                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

    def get_default_gateway_windows(self):
        if 1 == 0:
            try:
                import ctypes
            except ImportError:
                print (modulname + " ctypes failed")
            def is_admin():
                try:
                    return ctypes.windll.shell32.IsUserAnAdmin()
                except:
                    return False
            if is_admin():
                print (modulname + "is_admin: yes")
            else:
                print (modulname + "is_admin: no, try runas now...")
                # Re-run the program with admin rights __file__
                #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            try:
                import wmi
                wmi_obj = wmi.WMI()
                wmi_sql = 'select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE'
                wmi_out = wmi_obj.query( wmi_sql )
                for dev in wmi_out:
                    print (modulname + " IPv4Address: %s" % str(dev.IPAddress[0]))
                    print (modulname + " DefaultIPGateway: %s" % str(dev.DefaultIPGateway[0]))
            except ImportError:
                print (modulname + " import wmi failed and not windows DefaultIPGateway possible")
    #        try:
    #            import win32com.client
    #        except ImportError:
    #            print ("jk-import win32com.client failed and not windows DefaultIPGateway possible")
    #        try:
    #            import wmi_client_wrapper as wmi
    #        except ImportError:
    #            print ("jk-import wmi_client_wrapper failed and not windows DefaultIPGateway possible")
    ################################################################################################################
    def do_ping(ip):
        address = [ip]
        retvalue = 1
        if sys.platform == "win32":
            #response = os.system("ping -n 1 -l 1 -w 100 " + ip + ">nul")
            #response = os.system("cmd /c START /MIN cmd /k ( ping -n 1 -l 1 -w 100 " + ip + " )")
            response = 0
            if response == 0:
                retvalue = 0
            else:
                retvalue = 1
            ping_args = ["ping", "-n", "1", "-l", "1", "-w", "100"]
            try:
                ping = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                out, error = ping.communicate()
                printout = str(out)
                if printout.find('TTL') != -1:
                    retvalue = 0
                elif 'ttl' in printout:
                    retvalue = 0
                else:
                    retvalue = 1
            except:
                traceback.print_exc()
                retvalue = 1
        else:
            #ping_args = ["ping", "-c", "1", "-l", "1", "-s", "1", "-W", "1"]
            #ping = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
            response = os.system("ping -c 1 -l 1 -s 1 -W 1 " + ip + " > /dev/null 2>&1")
            #response = os.system("ping -c 1 -w2 " + ip + " > /dev/null 2>&1")
            #"astraceroute -H microsoft.com -p 80 -i eth1"
            if response == 0:
                retvalue = 0
            else:
                retvalue = 1
        return retvalue
#######################################################
    def do_tcp_ping(ip,port):
        retvalue = 1
        socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = socket_obj.connect_ex((ip,port))
        socket_obj.close()
        if result == 0:
            retvalue = 0
        else:
            retvalue = 1
        return retvalue

    def ping_socket(ip, port=80):
        retvalue = 0
        response = 0
        time_diff= 0
        try:
            #start_time = time.clock()
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip,port))
            sock.close()
            #time_diff = time.clock() - start_time
            time_diff = time.time() - start_time
            #print ("time ping_socket : %s seconds" % str(time_diff))
            #print ("time ping_socket : %s" % str(int(round(time_diff * 1000))) + ' ' + str(ip))
            retvalue = int(round(time_diff * 1000))
        except:
            traceback.print_exc()
            retvalue = 0
        return retvalue
#######################################################
    
    
###############################################################################################################
if __name__ == '__main__':
    print (modulname + ": in main")
    root.mainloop()
    exitfunc()
    #root.destroy()
