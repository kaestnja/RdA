import os
import time
import signal
import subprocess
import psutil
#########################################################
# Map child PID to Popen object
SUBPROCESSES = {}
# Define handler
def handle_sigchld(signum, frame):
    pid = os.wait()[0]
    print ('Subprocess PID=%d ended', pid)
    del SUBPROCESSES[pid]
# Handle SIGCHLD
signal.signal(signal.SIGCHLD, handle_sigchld)
# Spawn a couple of subprocesses
p1 = subprocess.Popen(['sleep', '1'])
SUBPROCESSES[p1.pid] = p1
p2 = subprocess.Popen(['sleep', '2'])
SUBPROCESSES[p2.pid] = p2

# Wait for all subprocesses to die
while SUBPROCESSES:
    print ('tick')
    time.sleep(1)
# Done
print ('All subprocesses died')
#########################################################
proc = subprocess.Popen(...)
try:
    outs, errs = proc.communicate(timeout=15)
except TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()
#########################################################
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()
proc = subprocess.Popen(["infinite_app", "param"], shell=True)
try:
    proc.wait(timeout=3)
except subprocess.TimeoutExpired:
    kill(proc.pid)
#########################################################
count = 0
while True:
    count = count + 1
    print("loop: " + str(count))
    subprocess.call('pgrep -x "omxplayer" > /dev/null 2>&1', shell=True)
    time.sleep(0.05)
#########################################################
cmd = 'pgrep -x "omxplayer" > /dev/null 2>&1'
p = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
p.kill()