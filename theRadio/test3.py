import os
import psutil

from multiprocessing import Process
from time import sleep


class MyProcessAbstraction(object):
    def __init__(self, parent_pid, command):
        """
        @type parent_pid: int
        @type command: str
        """
        self._child = None
        self._cmd = command
        self._parent = psutil.Process(pid=parent_pid)

    def run_child(self):
        """
        Start a child process by running self._cmd. 
        Wait until the parent process (self._parent) has died, then kill the 
        child.
        """
        print ('---- Running command: "%s" ----' % self._cmd)
        self._child = psutil.Popen(self._cmd)
        try:
            while self._parent.status == psutil.STATUS_RUNNING:
                sleep(1)
        except psutil.NoSuchProcess:
            pass
        finally:
            print ('---- Terminating child PID %s ----' % self._child.pid)
            self._child.terminate()


if __name__ == "__main__":
    parent = os.getpid()
    child = MyProcessAbstraction(parent, 'ping -t localhost')
    child_proc = Process(target=child.run_child)
    child_proc.daemon = True
    child_proc.start()

    print ('---- Try killing PID: %s ----' % parent)
    while True:
        sleep(1)
