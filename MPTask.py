#!./mypy/bin/python
import multiprocessing as mp
import random
import time

class MPTask:

    def __init__ (self, func, **kwargs):
        print ("Creating an mpTask...")
        self.function = func
        #self.argTupple = (v for k,v in kwargs.items())
        self.proc = 1
        self.argDict = kwargs
        self.isdaemon = False
        self.name = 'def'

    def set_proc (self, n=1):
        self.proc = n

    def isDaemon (self, isd=False):
        self.isdaemon = isd


class MPTaskExecute:

    def __init__ (self, mp_task_list=[]):
        self.mp_task_list = mp_task_list
        self.proc = 2
        self.procs = []

    def set_proc (self, n):
        self.proc = n

    def _run_proc (self, mpTask):
        proc = mp.Process ( 
                            group = None,
                            name = mpTask.name,
                            target = mpTask.function, 
                            #args = mpTask.argTupple,
                            kwargs = mpTask.argDict)
        if (mpTask.isdaemon):
            proc.daemon = True
        return proc

    def start (self, force=0):
        self.procs = []
        for mpTask in self.mp_task_list:
            if force == 0:
                proc = self._run_proc (mpTask)
                self.procs.append (proc)
                proc.start ()
            else:
                procs_alive = [1 for proc in self.procs if proc.is_alive() ]
                while (len(procs_alive) >= force):
                    time.sleep (0.5)
                    procs_alive = [1 for proc in self.procs if proc.is_alive() ]
                proc = self._run_proc (mpTask)
                self.procs.append (proc)
                proc.start ()

    def join (self):
        for proc in self.procs:
            proc.join()

    def terminate (self):
        for proc in self.procs:
            proc.terminate()

def func (arg='',sec='',thi=''):
  t = random.randrange (1,10)
  print ("starting ",arg," delay ",t,' sec ',sec,' thi ',thi)
  time.sleep (t)
  print ("ending ",arg)

if __name__ == '__main__':

    mptl = []

    for i in range (1,10):
        print ("------------------- ",i)
        mptl.append ( MPTask (func,
                             arg='Name{}'.format(i),
                             thi='THI{}'.format(i)
                            )
                    )

    mpte = MPTaskExecute (mptl)
    mpte.start (force=3)
    mpte.join ()

