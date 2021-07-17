#!/usr/bin/python3
version=153
#https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe 
#to better debug: on crash enter: import pdb; pdb.pm()
#maybe change from "/usr/bin/env python3" to "/usr/bin/python3"
import os, sys, math, string, struct, socket, time, datetime, traceback, subprocess, pathlib
import ftplib, contextlib, shutil
if sys.version[0] == '2':
    sys.exit() #exit with exception, used to exit treads
global the_hostname
the_hostname = socket.gethostname()

if not ('test51' in the_hostname or 'sky' in the_hostname):
    print ('jk-the_hostname %s is not test51 or sky!' % the_hostname)
    quit()
    sys.exit() #exit with exception, used to exit treads

if not os.path.isdir(sys.path[0]):
    print ('jk-sys.path[0] %s is not a directory!' % sys.path[0])
    sys.exit() #exit with exception, used to exit treads
if pathlib.Path(sys.path[0]).exists:
    if not pathlib.Path(sys.path[0]).is_dir:
        print ('jk-sys.path[0] is not dir (pathlib) %s' % sys.path[0])
        sys.exit() #exit with exception, used to exit treads
else:
    print ('jk-sys.path[0] not exist (pathlib) %s' % sys.path[0])
    sys.exit() #exit with exception, used to exit treads
###########################################################################
def exit(event):
    exitfunc()
def on_closing():
    exitfunc()
def exitfunc():
    print ('jk-This last via exitfunc')
    quit()
sys.exitfunc = exitfunc
########################################################################################
import pysftp #pip3 install pysftp
import requests #pip3 install requests
import urllib.parse    #from urllib.parse import urlsplit, urlunsplit
import urllib.request
global cnopts
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
####################################################################
def ftplib_placeFile(temp_ftpserver,temp_username, temp_password, temp_ftpfolder,temp_ftpfilename,temp_localfolder,temp_localfilename):
    #with contextlib.closing(ftplib.FTP('snakekiller.de')) as ftp:
    with contextlib.closing(ftplib.FTP()) as ftp:
        #ftp = FTP('snakekiller.de')
        try:
            ftp0_return1 = ftp.connect(host=temp_ftpserver)
            if not ftp0_return1.startswith('220 FTP Server ready'):
                print ('jk-ftplib_placeFile--ftp.getwelcome failed: %s' % str(ftp0_return1))
                ftp.quit()
                return False
            ftp0_return2 = ftp.getwelcome()
            if not ftp0_return2.startswith('220 FTP Server ready'):
                print ('jk-ftplib_placeFile--ftp.getwelcome failed: %s' % str(ftp0_return2))
                ftp.quit()
                return False
            ftp1_return1 = ftp.login(user='root', passwd = 'toor')
            if not ftp1_return1.startswith('230 User'):
                print ('jk-ftplib_placeFile--ftp.login failed: %s' % str(ftp1_return1))
                ftp.quit()
                return False
            #ftp1_return2 = ftp.retrlines('LIST')
            ##print ('ftp1_return2: %s' % ftp1_return2)
            #if not ftp1_return2.startswith('226 Transfer complete'):
            #    print ('jk---ftp LIST failed: %s' % str(ftp1_return2))
            #ftp.cwd('/radio/download/')
            ftp1_return3 = ftp.cwd(temp_ftpfolder)
            if not ftp1_return3.startswith('250 CWD command successful'):
                print ('jk-ftplib_placeFile--ftp CWD failed: %s' % str(ftp1_return3))
                ftp.quit()
                return False
            #wdir = ftp.sendcmd('PWD')
            #print (ftplib.parse257(wdir))
            #print ('jk---ftp PWD: %s' % str(ftplib.parse257(wdir)))
            #wdir2 = ftp.pwd()
            #print (wdir2)
            #print ('jk---ftp.pwd: %s' % str(ftp.pwd()))
            with open(os.path.join(temp_localfolder, temp_filename), 'rb') as fp:
                ftp1_return5 = ftp.storbinary('STOR ' + temp_filename, fp)
                if not ftp1_return5.startswith('226 Transfer complete'):
                    print ('jk-ftplib_placeFile--ftp Upload failed: %s' % str(ftp1_return5))
                    ftp.quit()
                else:
                    ftp.quit()
                    return True
        except ftplib.all_errors as e:
            print ('jk-ftplib_placeFile ftp error:', e)
        except TimeoutError:
            print ('jk-ftplib_placeFile ftp TimeoutError')
        except:
            print ('jk-ftplib_placeFile ftp unknown Error')
    return False
####################################################################
        #https://stackoverflow.com/questions/38939454/verify-host-key-with-pysftp
        #http://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html#pysftp-cnopts
        #https://gist.github.com/johnfink8/2190472
def sftp_placeFile(temp_ftpfolder,temp_ftpfilename,temp_localfolder,temp_localfilename,srv_sftp):
    retvalue = 1
    retvalue1 = 1
    retvalue2 = 1
    retvalue3 = 1
    local_path = temp_localfolder + '/' + temp_localfilename
    print ('jk-sftp_placeFile to: %s' % (str(temp_ftpfilename)))
    local_file = pathlib.Path(local_path)
    if (local_file.is_file() and srv_sftp): #srv_sftp.exists(temp_ftpfolder)):
        remote_path = temp_ftpfolder + temp_ftpfilename
        srv_sftp.chdir(temp_ftpfolder)  # change directory on remote server
        # Prints out the directories and files, line by line
        #data = srv_sftp.listdir()
        #for i in data:
            #print ('jk--remote file:  %s' % i)
            #if temp_ftpfilename in i:
                #print ('jk--sftp_placeFile remote file found before upload: %s' % i)
        #with srv_sftp.cd(temp_ftpfolder):
            #srv_sftp.put(local_path)  # To download a file, replace put with get
        srv_sftp.put(local_path, remote_path)
        srv_sftp.chdir(temp_ftpfolder)  # change directory on remote server
        #data1 = srv_sftp.listdir(remotepath=temp_ftpfolder)
        data1 = srv_sftp.listdir()
        for i1 in data1:
            if temp_ftpfilename in str(i1):
                if srv_sftp.isfile(remote_path):
                    #print ('jk--sftp_placeFile remote file found after upload: %s' % i1)
                    retvalue1 = 0
                    break
        if retvalue1==0:
            srv_sftp.chdir(temp_ftpfolder)  # change directory on remote server
            if (temp_localfilename.endswith('py') or temp_localfilename.endswith('sh')):
                srv_sftp.chmod(remote_path, 6777)
            else:
                srv_sftp.chmod(remote_path, 666)
            srv_sftp.chdir(temp_ftpfolder)  # change directory on remote server
            #data2 = srv_sftp.listdir_attr()
            data2 = srv_sftp.listdir_attr(remotepath=temp_ftpfolder)
            temp_mod_line = ''
            for i2 in data2:
                if temp_ftpfilename in str(i2):
                    #print ('jk--sftp_placeFile remote file attributs: %s' % str(i2))
                    if '1000     1000' in str(i2):
                        retvalue2 = 0
                    if ('-rwxrwxrwx' in str(i2)) and ((temp_localfilename.endswith('py') or temp_localfilename.endswith('sh'))):
                        retvalue3 = 0
                    elif '-rw-r--r--' in str(i2):
                        retvalue3 = 0
                    elif ('-rw-rw-rw-' in str(i2)) and ((temp_localfilename.endswith('txt') or temp_localfilename.endswith('desktop'))):
                        retvalue3 = 0
                    else:
                        temp_mod_line = str(i2)
                    break
            if not retvalue2==0:
                print ('jk-sftp_placeFile maybe wrong own: %s' % remote_path)
            if not retvalue3==0:
                print ('jk-sftp_placeFile wrong mod: %s %s' % (remote_path, temp_mod_line))
        else:
            print ('jk-sftp_placeFile not a file: %s' % remote_path)
    else:
        print ('jk-sftp_placeFile temp_ftpfolder not found: %s' % temp_ftpfolder)
    return retvalue
####################################################################
def sftp_command_return(temp_ftpserver,temp_username, temp_password, temp_command):
    print ('jk-sftp_command_return:  %s %s' % (temp_ftpserver, temp_command))
    retvalue = 1
    global cnopts
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(host=temp_ftpserver,username=temp_username,password=temp_password,cnopts=cnopts) as srv_sftp:
            #print ('jk--sftp_command_return:  %s' % (str(srv_sftp.execute("DISPLAY=:0 nohup shopt -q login_shell && echo 'Login shell' || echo 'No login shell'"))))
            print ('jk-sftp_command_return:  %s' % (str(srv_sftp.execute(temp_command))))
            retvalue = 0
    except:
        retvalue = 1
        print ('jk-sftp_command_return exception:  %s' % temp_command)
    finally:
        srv_sftp.close()
    return retvalue
####################################################################
def sftp_command(temp_ftpserver,temp_username, temp_password, temp_command):
    print ('jk-sftp_command:  %s %s' % (temp_ftpserver, temp_command))
    retvalue = 1
    global cnopts
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(host=temp_ftpserver,username=temp_username,password=temp_password,cnopts=cnopts) as srv_sftp:
            srv_sftp.execute(temp_command)
            retvalue = 0
            srv_sftp.close()
    except:
        retvalue = 1
        print ('jk-sftp_command exception:  %s' % temp_command)
    finally:
        return retvalue
####################################################################
def do_ping(ip):
    address = [ip]
    retvalue = 1
    if sys.platform == "win32":
        response = os.system("ping -n 1 -l 1 -w 100 " + ip + ">nul")
        #response = os.system("cmd /c START /MIN cmd /k ( ping -n 1 -l 1 -w 100 " + ip + " )")
        response = 0
        if response == 0:
            retvalue = 0
        else:
            retvalue = 1
        return retvalue
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
            retvalue = 1
    else:
        #ping_args = ["ping", "-c", "1", "-l", "1", "-s", "1", "-W", "1"]
        #ping = subprocess.Popen(ping_args + [address], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
        response = os.system("ping -c 1 -l 1 -s 1 -W 1 " + ip + " > /dev/null 2>&1")
        #response = os.system("ping -c 1 -w2 " + ip + " > /dev/null 2>&1")
        if response == 0:
            retvalue = 0
        else:
            retvalue = 1
    return retvalue
####################################################################
#http://www.bogotobogo.com/python/python_traversing_directory_tree_recursively_os_walk.php
#https://stackoverflow.com/questions/5663787/upload-folders-from-local-system-to-ftp-using-python-script
#https://stackoverflow.com/questions/32481640/how-do-i-upload-full-directory-on-ftp-in-python
#https://mayankjohri.wordpress.com/2008/07/02/create-list-of-files-in-a-dir-tree/
def sftp_placeFolders(ftpfolder,temp_localfolder, srv_sftp):
    retvalue = 1
    print ('jk--sftp_placeFolders from: %s to: %s' % (str(temp_localfolder), str(ftpfolder)))
    #from: D:\__Dropbox\Dropbox\aRadio\theRadio\aMagicEye to:  //home//pi//aRadio//theRadio
    if (srv_sftp is None):
        return retvalue
    if not(srv_sftp.isdir('//home//pi//aRadio')) :
        print ('jk--sftp_placeFiles folder mkdir:  %s' % ('//home//pi//aRadio'))
        srv_sftp.mkdir('//home//pi//aRadio')
        srv_sftp.chmod('//home//pi//aRadio', 6777)
    if not(srv_sftp.isdir('//home//pi//aRadio//theRadio')) :
        print ('jk--sftp_placeFiles folder mkdir:  %s' % ('//home//pi//aRadio//theRadio'))
        srv_sftp.mkdir('//home//pi//aRadio//theRadio')
        srv_sftp.chmod('//home//pi//aRadio//theRadio', 6777)
    if not srv_sftp.isdir(ftpfolder + '//' + os.path.basename(temp_localfolder)):
        print ('jk--sftp_placeFiles folder mkdir:  %s' % (ftpfolder + '//' + os.path.basename(temp_localfolder)))
        srv_sftp.mkdir(ftpfolder + '//' + os.path.basename(temp_localfolder))
        srv_sftp.chmod(ftpfolder + '//' + os.path.basename(temp_localfolder), 6777)

    for name in os.listdir(temp_localfolder):
        localpath = os.path.join(temp_localfolder, name)
        if os.path.isfile(localpath):
            print("STOR", localpath, ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name)
            srv_sftp.put(localpath,ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name)
##            if 'radio' in temp_ftpserver:
##                srv_sftp.chown(remote_path,1000,1000)
            if (name.endswith('py') or name.endswith('sh')):
                srv_sftp.chmod(ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name, 6777)
            if (name.endswith('ttf') or name.endswith('otf')):
                srv_sftp.chmod(ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name,2775)
                srv_sftp.chown(ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name,0,50)
        elif os.path.isdir(localpath):
            #print("MKD", name, localpath, ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name)
            if not srv_sftp.isdir(ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name):
                print ('jk--sftp_placeFiles folder mkdir:  %s' % (ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name))
                srv_sftp.mkdir(ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name)
                srv_sftp.chmod(ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name, 6777)
            if srv_sftp.isdir(ftpfolder + '//' + os.path.basename(temp_localfolder) + '//' + name):
                sftp_placeFolders(ftpfolder + '//' + os.path.basename(temp_localfolder),localpath,srv_sftp)

    #local_folder = pathlib.Path(temp_localfolder)
    #os.chdir(os.path.split(temp_localfolder)[0])
    #parent = os.path.split(temp_localfolder)[1]
    print ('::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    return retvalue
####################################################################
        #cnopts = pysftp.CnOpts()
        #cnopts.hostkeys = None
        #keydata = b"""AAAAB3NzaC1yc2EAAAADAQAB..."""
        #key = paramiko.RSAKey(data=decodebytes(keydata))
        #cnopts = pysftp.CnOpts()
        #cnopts.hostkeys.add('example.com', 'ssh-rsa', key)
        #srv_sftp = pysftp.Connection(host="janradio", username="root", password="toor", hostkeys = None)
        #with pysftp.Connection(host="janradio", username="root", password="toor", cnopts=cnopts) as srv_sftp:
def create_sftp(temp_ftpserver,temp_username, temp_password):
    retvalue = None
    global cnopts
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        #pysftp.Connection(host, username=None, private_key=None, password=None, port=22, private_key_pass=None, ciphers=None, log=False)
        temp_srv_sftp = pysftp.Connection(host=temp_ftpserver,username=temp_username,password=temp_password,cnopts=cnopts)
        #with pysftp.Connection(host=temp_ftpserver,username=temp_username,password=temp_password,cnopts=cnopts) as srv_sftp:
        retvalue = temp_srv_sftp
    except:
        print ('jk--create_sftp exception')
        #temp_srv_sftp.close()
    return retvalue
####################################################################
def update_commands(target):
    print ('jk--update_commands for:  %s starts here-------------------------------' % target)
    #sftp_command(target,"pi","toor","DISPLAY=:0 nohup shopt -q login_shell && echo 'Login shell' || echo 'No login shell'")
    srv_sftp_pi = create_sftp(target,"pi","toor")
    srv_sftp_root = create_sftp(target,"root","toor")
    if not srv_sftp_root is None:
        sftp_command(target,"root","toor",'sudo pkill -SIGKILL -f python')
        sftp_command(target,"root","toor",'sudo pkill -SIGKILL -f python3')
        sftp_command(target,"root","toor",'sudo pkill -SIGKILL -f omxplayer')
        time.sleep(1)
        #ps aux | grep python
        #pidof python
        #sudo kill -SIGTERM 3486
        #sudo kill -SIGKILL 3486
        #sftp_command_return(target,"root","toor",'ps -p $$')      #chsh #change loginshell
        #sftp_command_return(target,"root","toor","readlink -f /proc/$$/exe")
        #sftp_command_return(target,"root","toor","env | grep ^SHELL=")
        #sftp_command_return(target,"root","toor","echo $0")
        #sftp_command_return(target,"root","toor","echo $SHELL")
        #sftp_command(target,"root","toor",'sudo pkill -f bash')
        #sftp_placeFolders('//usr//local//share',os.path.join(sys.path[0],'fonts'),srv_sftp_root)
        #sftp_command(target,"root","toor",'sudo fc-cache -f')
        time.sleep(2)
    if not srv_sftp_pi is None:
        if 1 == 1:
            #sftp_placeFolders('//home//pi',os.path.join(sys.path[0],'Desktop'),srv_sftp_pi)
            sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aClock'),srv_sftp_pi)
            #sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aConfig'),srv_sftp_pi)
            sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aFrame'),srv_sftp_pi)
            sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aGauge'),srv_sftp_pi)
            sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aMagicEye'),srv_sftp_pi)
            sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aNixie'),srv_sftp_pi)
            sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aSound'),srv_sftp_pi)
            sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'bImages'),srv_sftp_pi)

        if 1 == 1:
            #sftp_placeFile('//home//pi//Desktop//','theupdate.sh',sys.path[0],'theupdate.sh',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','rpi1radio.py',sys.path[0],'rpi1radio.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','anneradio.py',sys.path[0],'anneradio.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','janradio.py',sys.path[0],'janradio.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','janradiogrid.py',sys.path[0],'janradiogrid.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jksip.py',sys.path[0],'jksip.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jksmeter360.py',sys.path[0],'jksmeter360.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jksmetermg.py',sys.path[0],'jksmetermg.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jksmeterva.py',sys.path[0],'jksmeterva.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jksmeterva_cpu.py',sys.path[0],'jksmeterva_cpu.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jkslistcycle.py',sys.path[0],'jkslistcycle.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jksnixieclock.py',sys.path[0],'jksnixieclock.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','jksinstall.py',sys.path[0],'jksinstall.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','meterit.py',sys.path[0],'meterit.py',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','senderlist.txt',sys.path[0],'senderlist.txt',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','Standard_Class.py',sys.path[0],'Standard_Class.py',srv_sftp_pi)
            #sftp_placeFolders('//home//pi//aRadio//theRadio',os.path.join(sys.path[0],'aNixie'),srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','startit.sh',sys.path[0],'startit.sh',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','switch_torestart.sh',sys.path[0],'switch_torestart.sh',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','switch_toupdate.sh',sys.path[0],'switch_toupdate.sh',srv_sftp_pi)
            sftp_placeFile('//home//pi//aRadio//theRadio//','theupdate.sh',sys.path[0],'theupdate.sh',srv_sftp_pi)
        #------------------------------------------------------------------------------------
      
    sftp_command(target,"root","toor",'sudo reboot')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/anneradio.py >/dev/null 2>&1&')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/janradiogrid.py >/dev/null 2>&1&')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/Standard_Class.py >/dev/null 2>&1&')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/gauge.py>/dev/null 2>&1&')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/jksnixieclock.py>/dev/null 2>&1&')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/jksmeterva_cpu.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/jksnixieclock.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/anneradio.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/jksmeterva_cpu.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/jksmeterva_cpu.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/jksmeterva_cpu.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/meterit.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 python3 /home/pi/aRadio/theRadio/rpi1radio.py')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup python3 /home/pi/aRadio/theRadio/tkinterclock.py >/dev/null 2>&1&')
    #sftp_command(target,"pi","toor","DISPLAY=:0 nohup shopt -q login_shell && echo 'Login shell' || echo 'No login shell'")
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup python3 /root/Dropbox/aRadio/theRadio/meterit.py >/dev/null 2>&1&')
    #sftp_command(target,"pi","toor",'DISPLAY=:0 nohup sh /home/pi/Desktop/theupdate.sh >/dev/null 2>&1&')
    if (srv_sftp_pi):
        srv_sftp_pi.close()
    if (srv_sftp_root):
        srv_sftp_root.close()

##    from pexpect import pxssh
##    #import pxssh
##    #import getpass
##    try:
##        s = pxssh.pxssh()
##        #hostname = raw_input('hostname: ')
##        #username = raw_input('username: ')
##        #password = getpass.getpass('password: ')
##        s.login (target,"root","toor")
##        s.sendline ('uptime')   # run a command
##        s.prompt()             # match the prompt
##        print (s.before)          # print everything before the prompt.
##        s.sendline ('ls -l')
##        s.prompt()
##        print (s.before)
##        s.sendline ('df')
##        s.prompt()
##        print (s.before)
##        s.logout()
##    except pxssh.ExceptionPxssh as e:
##        print ("pxssh failed on login.")
##        print (str(e))



if 'test51' in the_hostname:

    if 1==1:
        temptarget='rpi4'
        do_ping(temptarget)
        time.sleep(1)
        if do_ping(temptarget)==0:
            update_commands(temptarget)
    if 1==0:
        temptarget='rpi3'
        do_ping(temptarget)
        time.sleep(1)
        if do_ping(temptarget)==0:
            update_commands(temptarget)
    if 1==1:
        temptarget='rpi2'
        do_ping(temptarget)
        time.sleep(1)
        if do_ping(temptarget)==0:
            update_commands(temptarget)
    if 1==1:
        temptarget='rpi1'
        do_ping(temptarget)
        time.sleep(1)
        if do_ping(temptarget)==0:
            update_commands(temptarget)

if 'sky' in the_hostname:
    shutil.copyfile( os.path.join(sys.path[0],'theupdate.sh') , os.path.join('/root/Desktop','theupdate.sh') , follow_symlinks=False)

    temptarget='rpi1radio'
    do_ping(temptarget)
    time.sleep(1)
    if do_ping(temptarget)==0:
        update_commands(temptarget)

    temptarget='192.168.26.111'
    do_ping(temptarget)
    time.sleep(1)
    if do_ping(temptarget)==0:
        update_commands(temptarget)

#import psutil #https://github.com/giampaolo/psutil
#psutil.sensors_temperatures()

exit(0)
quit()
sys.exit(1)

#       ssh -n -f user@host "sh -c 'cd /whereever; nohup ./whatever > /dev/null 2>&1 &'"
#       ssh user@example.com 'nohup sleep 300 >/dev/null 2>/dev/null </dev/null &'
#       ssh user@example.com -t 'screen -D -RR -S this /bin/sleep 300'

def get_version_from_file(temp_path_file):
    result = 0
    temp_is_file = pathlib.Path(temp_path_file)
    if temp_is_file.is_file():
        result = 1
        #print ("    jk-get_version_from_file: %s" % temp_path_file)
        with open(temp_path_file,"r") as temp_file:
            for temp_line in temp_file:
                if temp_line.startswith('version') and temp_line.strip():
                    #rint ('jk-temp_line: %s' % temp_line)
                    (temp_key, temp_value) = temp_line.split("=")
                    temp_value = int(temp_value)
                    if temp_value > 1:
                        result = temp_value
                    break
    return result
####################################################################
#https://mein.1und1.de/DomainNGSettingsUpdate?__frame=_top&__lf=settings_flow
def grabFile(temp_ftpfolder,temp_localfolder,temp_filename,temp_localfilename):
    if not os.path.isfile(os.path.join(temp_localfolder, temp_localfilename)):
        if 1 == 1:
            # https://docs.python.org/3/library/ftplib.html
            #with ftplib.FTP('snakekiller.de') as ftp:
            with contextlib.closing(ftplib.FTP('snakekiller.de')) as ftp:
                try:
                    #ftp = ftplib.FTP('home11879675.1and1-data.host')
                    ftp1_return0 = ftp.getwelcome()
                    if not ftp1_return0.startswith('220 FTP Server ready'):
                        print ('jk---ftp.getwelcome failed: %s' % str(ftp1_return0))
                        ftp.quit()
                        return False
                    ftp1_return1 = ftp.login(user='1172-692', passwd = '-Brenda+Norre0808')
                    if not ftp1_return1.startswith('230 User'):
                        print ('jk---ftp.login failed: %s' % str(ftp1_return1))
                        ftp.quit()
                        return False
                    #ftp1_return2 = ftp.retrlines('LIST')
                    #if not ftp1_return2.startswith('226 Transfer complete'):
                    #    print ('jk---ftp LIST failed: %s' % str(ftp1_return2))
                    #ftp.cwd('/radio/download/')
                    ftp1_return3 = ftp.cwd(temp_ftpfolder)
                    if not ftp1_return3.startswith('250 CWD command successful'):
                        print ('jk---ftp CWD failed: %s' % str(ftp1_return3))
                        ftp.quit()
                        return False
                    #wdir = ftp.sendcmd('PWD')
                    #print (ftplib.parse257(wdir))
                    #print ('jk---ftp PWD: %s' % str(ftplib.parse257(wdir)))
                    #wdir2 = ftp.pwd()
                    #print (wdir2)
                    #print ('jk---ftp.pwd: %s' % str(ftp.pwd()))
                    #ftp1_return4 = ftp.retrlines('LIST')
                    #if not ftp1_return4.startswith('226 Transfer complete'):
                    #    print ('jk---ftp LIST failed: %s' % str(ftp1_return4))
                    if 1 == 1:
                        with open(os.path.join(temp_localfolder, temp_localfilename), 'wb') as localfile:
                            ftp1_return5 = ftp.retrbinary('RETR ' + temp_filename, localfile.write, 1024)
                            if not ftp1_return5.startswith('226 Transfer complete'):
                                print ('jk---ftp Download failed: %s' % str(ftp1_return5))
                                ftp1_return7 = localfile.close()
                                if os.path.isfile(os.path.join(temp_localfolder, temp_localfilename)):
                                    os.remove(os.path.join(temp_localfolder, temp_localfilename))
                                ftp.quit()
                                return False
                            else:
                                ftp1_return7 = localfile.close()
                                ftp1_return6 = ftp.quit()
                                if not ftp1_return6.startswith('221 Goodbye'):
                                    print ('jk---ftp.quit failed: %s' % str(ftp1_return6))
                                return True
                    else:
                        localfile = open(os.path.join(temp_localfolder, temp_localfilename), 'wb')
                        ftp1_return5 = ftp.retrbinary('RETR ' + temp_filename, localfile.write, 1024)
                        if not ftp1_return5.startswith('226 Transfer complete'):
                            print ('jk---ftp Download failed: %s' % str(ftp1_return5))
                            ftp1_return7 = localfile.close()
                            if os.path.isfile(os.path.join(temp_localfolder, temp_localfilename)):
                                os.remove(os.path.join(temp_localfolder, temp_localfilename))
                            ftp.quit()
                            return False
                        else:
                            ftp1_return7 = localfile.close()
                            ftp1_return6 = ftp.quit()
                            if not ftp1_return6.startswith('221 Goodbye'):
                                print ('jk---ftp.quit failed: %s' % str(ftp1_return6))
                            return True
                except ftplib.all_errors as e:
                    print ('jk--grabFile ftp error: %s' % str(e))
                except socket.error as e:
                    print ('jk--grabFile socket error: %s' % str(e))
                except TimeoutError:
                    print ('jk--grabFile ftp TimeoutError')
                except:
                    print ('jk--grabFile ftp unknown Error')
            ftp.quit()
            return False
        else:
            try:
                #urllib.request.urlretrieve('ftp://home11879675.1and1-data.host'+ temp_ftpfolder + temp_filename, os.path.join(temp_localfolder, temp_localfilename))
                urllib.request.urlretrieve('ftp://snakekiller.de'+ temp_ftpfolder + temp_filename, os.path.join(temp_localfolder, temp_localfilename))
                return True
            except:
                # https://docs.python.org/3/howto/urllib2.html
                # if you need to pass credentials:
                user = '1172-692'
                passwd = '-Brenda+Norre0808'
                #down_link = 'ftp://' + user + ':' + passwd + '@home11879675.1and1-data.host' + temp_ftpfolder.replace("//", "/") + temp_filename
                down_link = 'ftp://' + user + ':' + passwd + '@snakekiller.de' + temp_ftpfolder.replace("//", "/") + temp_filename
                target_file = os.path.join(temp_localfolder, temp_localfilename)
                print ('ftp2 down_link: %s' % down_link)
                #urllib.request.urlretrieve('ftp:////' + user + ':' + passwd + '@home11879675.1and1-data.host'+temp_ftpfolder, os.path.join(temp_localfolder, filename))
                #urllib.request.urlretrieve('ftp://1172-692:-Brenda+Norre0808@home11879675.1and1-data.host/radio/download/' + filename, os.path.join(temp_localfolder, filename))
                try:
                    ftp2_return1 = urllib.request.urlretrieve(down_link, target_file)
                    print ('ftp2_return1: %s' % ftp2_return1)
                    return True
                except:
                    print ('ftp2_return1 failed')
                    with urllib.request.urlopen(down_link) as d, open(target_file, "wb") as opfile:
                        data = d.read()
                        opfile.write(data)
                    return True
    else:
        print ('jk---grabFile Error: tempfile still exist, must be deleted before download a new version')
        return False
