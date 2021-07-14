import os
import time
import signal
import subprocess
import psutil

cmd = 'pgrep -x "omxplayer" > /dev/null 2>&1'
    
#########################################################
count = 0
while True:
    try:
        count = count + 1
        stime = time.strftime('%H:%M:%S')
        p2 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
        # p2 = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # out, err = p2.communicate()[0]
        p2output = p2.communicate()[0]
        print(stime + " loop: " + str(count) + " p2return:" + str(p2.returncode))
        # print ('stdout: ' + out)
        # print ('stderr: ' + err)
        p2.kill()
        time.sleep(0.05)
    except:
        break

#########################################################
# https://docs.python.org/3.7/library/subprocess.html
# how to use:https://www.tornadoweb.org/en/stable/_modules/subprocess.html
# https://bugs.python.org/review/26741/diff/16954/Lib/subprocess.py
count = 0
while True:
    try:
        count = count + 1
        stime = time.strftime('%H:%M:%S')
        p1return = subprocess.call('pgrep -x "omxplayer" > /dev/null 2>&1', shell=True)
        print(stime + " loop: " + str(count) + " p1return:" + str(p1return))
        time.sleep(0.05)
    except:
        break
